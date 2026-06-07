import uuid
import datetime
from datetime import UTC
from .task_queue import TaskQueue
from backend.logger import get_logger

AVAILABLE_AGENTS = ["research", "rag", "critic", "coding", "browser"]

class Dispatcher:
    def __init__(self):
        self.queue  = TaskQueue()
        self.logger = get_logger("orchestrator.dispatcher")

    def dispatch(self, task_id: str, subtasks: list[dict]) -> list[dict]:
        dispatched = []
        skipped    = []

        independent = [s for s in subtasks if not s.get("depends_on")]
        dependent   = [s for s in subtasks if s.get("depends_on")]

        for subtask in independent + dependent:
            result = self._push_job(task_id, subtask)
            if result:
                dispatched.append(result)
            else:
                skipped.append(subtask.get("subtask_id"))

        self.logger.info(f"Dispatch complete — {len(dispatched)} queued, {len(skipped)} skipped for task {task_id}")
        return dispatched

    def _push_job(self, task_id: str, subtask: dict) -> dict | None:
        agent = subtask.get("agent")
        if agent not in AVAILABLE_AGENTS:
            self.logger.warning(f"Unknown agent '{agent}' — skipping subtask {subtask.get('subtask_id')}")
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
            "dispatched_at": str(datetime.datetime.now(UTC))
        }

        if self.queue.push(job):
            self.logger.info(f"Queued subtask {subtask.get('subtask_id')} → {agent}")
            return job
        else:
            self.logger.error(f"Failed to queue subtask {subtask.get('subtask_id')}")
            return None

    def get_queue_size(self) -> int:
        return self.queue.size()

    def get_pending_jobs(self) -> list:
        return self.queue.peek()

    def clear_queue(self) -> bool:
        return self.queue.clear()