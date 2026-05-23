import uuid
import datetime
from .task_queue import TaskQueue

AVAILABLE_AGENTS = ["research", "rag", "critic", "coding", "browser"]

class Dispatcher:
    def __init__(self):
        self.queue = TaskQueue()

    def dispatch(self, task_id: str, subtasks: list[dict]) -> list[dict]:
        """Route subtasks to agents via the task queue respecting dependencies"""
        dispatched = []
        skipped    = []

        # Separate independent and dependent subtasks
        independent = [s for s in subtasks if not s.get("depends_on")]
        dependent   = [s for s in subtasks if s.get("depends_on")]

        # Push independent subtasks first
        for subtask in independent:
            result = self._push_job(task_id, subtask)
            if result:
                dispatched.append(result)
            else:
                skipped.append(subtask.get("subtask_id"))

        # Push dependent subtasks after
        for subtask in dependent:
            result = self._push_job(task_id, subtask)
            if result:
                dispatched.append(result)
            else:
                skipped.append(subtask.get("subtask_id"))

        # Summary log
        print(f"📋 Dispatch summary — {len(dispatched)} queued, {len(skipped)} skipped")
        if skipped:
            print(f"⚠️  Skipped subtask IDs: {skipped}")

        return dispatched

    def _push_job(self, task_id: str, subtask: dict) -> dict | None:
        """Build and push a single job to the queue"""
        agent = subtask.get("agent")

        if agent not in AVAILABLE_AGENTS:
            print(f"⚠️  Unknown agent '{agent}' — skipping subtask {subtask.get('subtask_id')}")
            return None

        job = {
            "job_id"       : str(uuid.uuid4()),
            "task_id"      : task_id,
            "subtask_id"   : subtask.get("subtask_id"),
            "title"        : subtask.get("title"),
            "description"  : subtask.get("description"),
            "agent"        : agent,
            "depends_on"   : subtask.get("depends_on", []),
            "status"       : "queued",
            "retry_count"  : 0,
            "dispatched_at": str(datetime.datetime.now(datetime.UTC))
        }

        if self.queue.push(job):
            print(f"✅ Queued subtask {subtask.get('subtask_id')} → {agent} agent")
            return job
        else:
            print(f"❌ Failed to queue subtask {subtask.get('subtask_id')}")
            return None

    def get_queue_size(self) -> int:
        return self.queue.size()

    def get_pending_jobs(self) -> list:
        return self.queue.peek()

    def clear_queue(self) -> bool:
        """Clear all pending jobs — useful for testing"""
        return self.queue.clear()