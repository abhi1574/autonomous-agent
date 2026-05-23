import os
import datetime
from datetime import UTC
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from agents.orchestrator.task_queue import TaskQueue
from memory.task_memory import TaskMemory
from memory.vector_store import VectorStore
from backend.models.task import TaskStatus

load_dotenv()

class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name  = agent_name
        self.queue       = TaskQueue()
        self.task_memory = TaskMemory()
        self.vector      = VectorStore()
        self._router     = None  # lazy loaded

    @property
    def router(self):
        """Lazy load to avoid circular imports"""
        if self._router is None:
            from tools.router import get_router
            self._router = get_router()
        return self._router

    @abstractmethod
    def execute(self, job: dict) -> str:
        pass

    def run(self):
        """Continuously pull jobs from queue and execute"""
        print(f"🤖 {self.agent_name} agent started — waiting for jobs...")

        while True:
            job = self.queue.pop()
            if not job:
                continue

            # Only process jobs meant for this agent
            if job.get("agent") != self.agent_name:
                self.queue.push(job)
                continue

            task_id    = job.get("task_id")
            subtask_id = job.get("subtask_id")
            depends_on = job.get("depends_on", [])

            # Check if dependencies are met
            if not self.queue.dependencies_met(task_id, depends_on):
                print(f"⏳ {self.agent_name} — dependencies not met for subtask {subtask_id}, re-queuing...")
                job["retry_count"] = job.get("retry_count", 0) + 1

                # Drop job if retried too many times — avoid infinite loop
                if job["retry_count"] > 10:
                    print(f"❌ Subtask {subtask_id} exceeded retry limit — dropping")
                    self.task_memory.update_task_status(
                        task_id=task_id,
                        status=TaskStatus.failed,
                        result=f"Subtask {subtask_id} dependencies never resolved"
                    )
                    continue

                self.queue.push(job)
                continue

            print(f"⚙️  {self.agent_name} picked up subtask {subtask_id}: {job.get('title')}")

            try:
                result    = self.execute(job)
                embedding = self.router.embed(result[:512])

                # Store result in PostgreSQL
                self.task_memory.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.completed,
                    result=result
                )

                # Store result in Qdrant
                self.vector.store(
                    text    = result,
                    metadata= {
                        "agent"     : self.agent_name,
                        "task_id"   : task_id,
                        "job_id"    : job.get("job_id"),
                        "subtask_id": subtask_id,
                        "title"     : job.get("title"),
                        "timestamp" : str(datetime.datetime.now(UTC))
                    },
                    vector  = embedding
                )

                # Mark subtask complete in Redis
                self.queue.mark_completed(task_id, subtask_id)

                print(f"✅ {self.agent_name} completed subtask {subtask_id}: {job.get('title')}")

            except Exception as e:
                print(f"❌ {self.agent_name} failed subtask {subtask_id}: {e}")
                self.task_memory.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.failed,
                    result=str(e)
                )

    def test_execute(self, job: dict) -> str:
        """For testing only — runs execute() and stores result to Qdrant"""
        result    = self.execute(job)
        embedding = self.router.embed(result[:512])

        self.vector.store(
            text    = result,
            metadata= {
                "agent"    : self.agent_name,
                "task_id"  : job.get("task_id"),
                "job_id"   : job.get("job_id"),
                "title"    : job.get("title"),
                "timestamp": str(datetime.datetime.now(UTC))
            },
            vector  = embedding
        )
        print(f"💾 Stored result to Qdrant for task: {job.get('task_id')}")
        return result