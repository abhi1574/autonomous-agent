import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TaskQueue:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )
        self.queue_name = "task_queue"

    def push(self, task: dict) -> bool:
        """Push a task to the queue"""
        try:
            self.client.lpush(self.queue_name, json.dumps(task))
            return True
        except Exception as e:
            print(f"❌ Queue push failed: {e}")
            return False

    def pop(self) -> dict | None:
        """Pop a task from the queue (blocking, waits 5s)"""
        try:
            result = self.client.brpop(self.queue_name, timeout=5)
            if result:
                _, data = result
                return json.loads(data)
            return None
        except Exception as e:
            print(f"❌ Queue pop failed: {e}")
            return None

    def peek(self) -> list:
        """See all pending tasks without removing them"""
        try:
            items = self.client.lrange(self.queue_name, 0, -1)
            return [json.loads(i) for i in items]
        except Exception as e:
            print(f"❌ Queue peek failed: {e}")
            return []

    def size(self) -> int:
        """How many tasks are waiting"""
        return self.client.llen(self.queue_name)

    def clear(self) -> bool:
        """Clear the queue"""
        try:
            self.client.delete(self.queue_name)
            return True
        except Exception as e:
            print(f"❌ Queue clear failed: {e}")
            return False