from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from uuid import UUID
from ..models.database import get_db
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskResponse
from ..middleware.auth import verify_token
from ..websocket.manager import manager

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    task = Task(title=payload.title, description=payload.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    return db.query(Task).order_by(Task.created_at.desc()).all()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_to_client(client_id, {
                "event": "echo",
                "data": data
            })
    except WebSocketDisconnect:
        manager.disconnect(client_id)