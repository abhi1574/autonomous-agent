import datetime
from datetime import UTC
from sqlalchemy.orm import Session
from backend.models.database import SessionLocal
from backend.models.task import Task, TaskStatus
from backend.logger import get_logger

class TaskMemory:
    def __init__(self):
        self.logger = get_logger("memory.task")

    def get_db(self) -> Session:
        return SessionLocal()

    def update_task_status(self, task_id: str, status: TaskStatus, result: str = None):
        db = self.get_db()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status     = status
                task.updated_at = datetime.datetime.now(UTC)
                if result:
                    task.result = result
                db.commit()
                self.logger.info(f"Task {task_id} status → {status.value}")
            else:
                self.logger.warning(f"Task {task_id} not found")
        except Exception as e:
            db.rollback()
            self.logger.error(f"TaskMemory update failed: {e}")
        finally:
            db.close()

    def get_task(self, task_id: str) -> dict | None:
        db = self.get_db()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                return {
                    "id"         : str(task.id),
                    "title"      : task.title,
                    "description": task.description,
                    "status"     : task.status,
                    "result"     : task.result,
                    "created_at" : str(task.created_at),
                    "updated_at" : str(task.updated_at),
                }
            return None
        except Exception as e:
            self.logger.error(f"TaskMemory get failed: {e}")
            return None
        finally:
            db.close()