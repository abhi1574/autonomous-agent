import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

class TaskQueue:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "").strip()

        if redis_url and redis_url.startswith(("redis://", "rediss://", "unix://")):
            self.client = redis.from_url(
                redis_url,
                decode_responses=True,
                ssl=redis_url.startswith("rediss://")
            )
        else:
            self.client = redis.Redis(
                host            =os.getenv("REDIS_HOST", "localhost"),
                port            =int(os.getenv("REDIS_PORT", 6379)),
                decode_responses=True
            )

        self.queue_name = "task_queue"

    def push(self, job: dict) -> bool:
        try:
            self.client.rpush(self.queue_name, json.dumps(job))
            return True
        except Exception:
            return False

    def pop(self, timeout: int = 5):
        try:
            result = self.client.blpop(self.queue_name, timeout=timeout)
            if result:
                return json.loads(result[1])
            return None
        except Exception:
            return None

    def peek(self) -> list:
        try:
            items = self.client.lrange(self.queue_name, 0, -1)
            return [json.loads(i) for i in items]
        except Exception:
            return []

    def size(self) -> int:
        try:
            return self.client.llen(self.queue_name)
        except Exception:
            return 0

    def clear(self) -> bool:
        try:
            self.client.delete(self.queue_name)
            return True
        except Exception:
            return False

    def mark_completed(self, task_id: str, subtask_id: str):
        key = f"completed:{task_id}"
        self.client.sadd(key, str(subtask_id))
        self.client.expire(key, 86400)
        print(f"✅ Marked subtask {subtask_id} complete for task {task_id}")

    def get_completed(self, task_id: str) -> set:
        key = f"completed:{task_id}"
        return {str(item) for item in self.client.smembers(key)}

    def dependencies_met(self, task_id: str, depends_on: list) -> bool:
        if not depends_on:
            return True
        completed   = self.get_completed(task_id)
        depends_str = {str(d) for d in depends_on}
        return depends_str.issubset(completed)