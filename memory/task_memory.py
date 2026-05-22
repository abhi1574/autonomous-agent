import os
import json
import datetime
from sqlalchemy.orm import Session
from backend.models.database import SessionLocal
from backend.models.task import Task, TaskStatus
from dotenv import load_dotenv

load_dotenv()

class TaskMemory:
    def get_db(self) -> Session:
        return SessionLocal()

    def update_task_status(self, task_id: str, status: TaskStatus, result: str = None):
        """Update task status in PostgreSQL"""
        db = self.get_db()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status     = status
                task.updated_at = datetime.datetime.utcnow()
                if result:
                    task.result = result
                db.commit()
                print(f"✅ Task {task_id} status → {status.value}")
            else:
                print(f"❌ Task {task_id} not found")
        except Exception as e:
            db.rollback()
            print(f"❌ TaskMemory update failed: {e}")
        finally:
            db.close()

    def get_task(self, task_id: str) -> dict | None:
        """Fetch a task from PostgreSQL"""
        db = self.get_db()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                return {
                    "id"          : str(task.id),
                    "title"       : task.title,
                    "description" : task.description,
                    "status"      : task.status,
                    "result"      : task.result,
                    "created_at"  : str(task.created_at),
                    "updated_at"  : str(task.updated_at),
                }
            return None
        finally:
            db.close()