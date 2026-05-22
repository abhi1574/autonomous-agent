import os
import uuid
import datetime
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

    @abstractmethod
    def execute(self, job: dict) -> str:
        """Each agent implements its own logic here"""
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
                self.queue.push(job)  # put it back
                continue

            print(f"⚙️  {self.agent_name} picked up job: {job.get('title')}")

            try:
                # Execute agent specific logic
                result = self.execute(job)

                # Store result in PostgreSQL
                self.task_memory.update_task_status(
                    task_id=job.get("task_id"),
                    status=TaskStatus.completed,
                    result=result
                )

                # Store result in Qdrant for future RAG
                self.vector.store(
                    text=result,
                    metadata={
                        "agent"     : self.agent_name,
                        "task_id"   : job.get("task_id"),
                        "job_id"    : job.get("job_id"),
                        "title"     : job.get("title"),
                        "timestamp" : str(datetime.datetime.utcnow())
                    },
                    vector=[0.0] * 384  # placeholder — real embeddings in Phase 5
                )

                print(f"✅ {self.agent_name} completed job: {job.get('title')}")

            except Exception as e:
                print(f"❌ {self.agent_name} failed job {job.get('job_id')}: {e}")
                self.task_memory.update_task_status(
                    task_id=job.get("task_id"),
                    status=TaskStatus.failed,
                    result=str(e)
                )