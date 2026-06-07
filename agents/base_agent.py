import datetime
from datetime import UTC
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from agents.orchestrator.task_queue import TaskQueue
from memory.task_memory import TaskMemory
from memory.vector_store import VectorStore
from backend.models.task import TaskStatus
from backend.logger import get_logger

load_dotenv()

class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name  = agent_name
        self.queue       = TaskQueue()
        self.task_memory = TaskMemory()
        self.vector      = VectorStore()
        self._router     = None
        self.logger      = get_logger(f"agent.{agent_name}")

    @property
    def router(self):
        if self._router is None:
            from tools.router import get_router
            self._router = get_router()
        return self._router

    @abstractmethod
    def execute(self, job: dict) -> str:
        pass

    def run(self):
        self.logger.info(f"Agent started — waiting for jobs")
        while True:
            job = self.queue.pop()
            if not job:
                continue

            if job.get("agent") != self.agent_name:
                self.queue.push(job)
                continue

            task_id    = job.get("task_id")
            subtask_id = job.get("subtask_id")
            depends_on = job.get("depends_on", [])

            if not self.queue.dependencies_met(task_id, depends_on):
                job["retry_count"] = job.get("retry_count", 0) + 1
                self.logger.warning(f"Dependencies not met for subtask {subtask_id} — retry {job['retry_count']}/10")

                if job["retry_count"] > 10:
                    self.logger.error(f"Subtask {subtask_id} exceeded retry limit — dropping")
                    self.task_memory.update_task_status(
                        task_id=task_id,
                        status =TaskStatus.failed,
                        result =f"Subtask {subtask_id} dependencies never resolved"
                    )
                    continue

                self.queue.push(job)
                continue

            self.logger.info(f"Picked up subtask {subtask_id}: {job.get('title')}")

            try:
                result    = self.execute(job)
                embedding = self.router.embed(result[:512])

                self.task_memory.update_task_status(
                    task_id=task_id,
                    status =TaskStatus.completed,
                    result =result
                )

                self.vector.store(
                    text    =result,
                    metadata={
                        "agent"     : self.agent_name,
                        "task_id"   : task_id,
                        "job_id"    : job.get("job_id"),
                        "subtask_id": subtask_id,
                        "title"     : job.get("title"),
                        "timestamp" : str(datetime.datetime.now(UTC))
                    },
                    vector=embedding
                )

                self.queue.mark_completed(task_id, subtask_id)
                self.logger.info(f"Completed subtask {subtask_id}: {job.get('title')}")

            except Exception as e:
                self.logger.error(f"Failed subtask {subtask_id}: {e}")
                self.task_memory.update_task_status(
                    task_id=task_id,
                    status =TaskStatus.failed,
                    result =str(e)
                )

    def test_execute(self, job: dict) -> str:
        result    = self.execute(job)
        embedding = self.router.embed(result[:512])
        self.vector.store(
            text    =result,
            metadata={
                "agent"    : self.agent_name,
                "task_id"  : job.get("task_id"),
                "job_id"   : job.get("job_id"),
                "title"    : job.get("title"),
                "timestamp": str(datetime.datetime.now(UTC))
            },
            vector=embedding
        )
        self.logger.info(f"test_execute stored result for task: {job.get('task_id')}")
        return result