import uuid
from .task_queue import TaskQueue

# Mock agents — Phase 4 will replace these with real implementations
AVAILABLE_AGENTS = ["research", "rag", "critic", "coding", "browser"]

class Dispatcher:
    def __init__(self):
        self.queue = TaskQueue()

    def dispatch(self, task_id: str, subtasks: list[dict]) -> list[dict]:
        """Route subtasks to agents via the task queue"""
        dispatched = []

        for subtask in subtasks:
            agent = subtask.get("agent")

            if agent not in AVAILABLE_AGENTS:
                print(f"⚠️ Unknown agent '{agent}' — skipping subtask {subtask.get('subtask_id')}")
                continue

            job = {
                "job_id"      : str(uuid.uuid4()),
                "task_id"     : task_id,
                "subtask_id"  : subtask.get("subtask_id"),
                "title"       : subtask.get("title"),
                "description" : subtask.get("description"),
                "agent"       : agent,
                "depends_on"  : subtask.get("depends_on", []),
                "status"      : "queued"
            }

            if self.queue.push(job):
                dispatched.append(job)
                print(f"✅ Dispatched subtask {subtask.get('subtask_id')} → {agent} agent")
            else:
                print(f"❌ Failed to dispatch subtask {subtask.get('subtask_id')}")

        return dispatched

    def get_queue_size(self) -> int:
        return self.queue.size()

    def get_pending_jobs(self) -> list:
        return self.queue.peek()