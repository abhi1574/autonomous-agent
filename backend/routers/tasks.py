from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Request
from sqlalchemy.orm import Session
from uuid import UUID
from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.models.database import get_db
from backend.models.task import Task, TaskStatus, ToolLog
from backend.schemas.task import TaskCreate, TaskResponse
from backend.middleware.auth import verify_token
from backend.websocket.manager import manager
from backend.logger import get_logger
from agents.orchestrator.planner import Planner
from agents.orchestrator.dispatcher import Dispatcher
from memory.task_memory import TaskMemory

router     = APIRouter()
limiter    = Limiter(key_func=get_remote_address)
logger     = get_logger("router.tasks")
planner    = Planner()
dispatcher = Dispatcher()
task_mem   = TaskMemory()

@router.post("/tasks", response_model=TaskResponse)
@limiter.limit("20/minute")
def create_task(
    request: Request,
    payload: TaskCreate,
    db     : Session = Depends(get_db),
    _      : dict    = Depends(verify_token)
):
    # Save task
    task = Task(title=payload.title, description=payload.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"Task created: {task.id} — {task.title}")

    # Plan subtasks
    subtasks = planner.plan(task.title, task.description or "")
    logger.info(f"Planner created {len(subtasks)} subtasks for task {task.id}")

    # Dispatch
    if subtasks:
        task_mem.update_task_status(str(task.id), TaskStatus.running)
        dispatcher.dispatch(str(task.id), subtasks)
        logger.info(f"Dispatched {len(subtasks)} subtasks for task {task.id}")

    return task

@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db), _: dict = Depends(verify_token)):
    return db.query(Task).order_by(Task.created_at.desc()).all()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, db: Session = Depends(get_db), _: dict = Depends(verify_token)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/tool-logs")
def get_tool_logs(db: Session = Depends(get_db), _: dict = Depends(verify_token)):
    logs = db.query(ToolLog).order_by(ToolLog.created_at.desc()).limit(50).all()
    return [
        {
            "id"         : str(log.id),
            "tool_name"  : log.tool_name,
            "agent_name" : log.agent_name,
            "task_id"    : log.task_id,
            "status"     : log.status,
            "duration_ms": log.duration_ms,
            "created_at" : str(log.created_at)
        }
        for log in logs
    ]

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    logger.info(f"WebSocket connected: {client_id}")
    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_to_client(client_id, {"event": "echo", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"WebSocket disconnected: {client_id}")