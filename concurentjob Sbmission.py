import threading
import time
from queue import Queue
from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Job:
    user_id: str
    job_id: str
    priority: int
    timestamp: float
    waiting_time: float = 0.0


class ConcurrentQueueManager:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = Queue(maxsize=capacity)
        self.job_counter = 0
        self.lock = threading.Lock()

    def generate_job_id(self) -> str:
        with self.lock:
            self.job_counter += 1
            return f"JOB-{self.job_counter:04d}"

    def enqueue(self, user_id: str, priority: int) -> Optional[Job]:
        if self.queue.full():
            return None

        job = Job(
            user_id=user_id,
            job_id=self.generate_job_id(),
            priority=priority,
            timestamp=time.time()
        )
        self.queue.put(job)
        return job

    def dequeue(self) -> Optional[Job]:
        if self.queue.empty():
            return None
        return self.queue.get()

    def process_simultaneous_submissions(self, submissions: List[tuple[str, int]]) -> List[Optional[Job]]:
        threads = []
        results = [None] * len(submissions)

        def worker(index, user_id, priority):
            job = self.enqueue(user_id, priority)
            results[index] = job

        for i, (user_id, priority) in enumerate(submissions):
            t = threading.Thread(target=worker, args=(i, user_id, priority))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results

    def get_queue_status(self) -> Dict:
        return {
            "size": self.queue.qsize(),
            "is_full": self.queue.full(),
            "is_empty": self.queue.empty(),
            "capacity": self.capacity
        }


if __name__ == "__main__":
    queue_manager = ConcurrentQueueManager(capacity=5)

    submissions = [
        ("user1", 1),
        ("user2", 2),
        ("user3", 1),
        ("user4", 3),
        ("user5", 2),
        ("user6", 1)  # Exceeds capacity
    ]

    results = queue_manager.process_simultaneous_submissions(submissions)

    for job in results:
        if job:
            print(f"Enqueued: Job ID: {job.job_id}, User ID: {job.user_id}, Priority: {job.priority}")
        else:
            print("Failed to enqueue a job due to full capacity.")

    print("Queue Status:", queue_manager.get_queue_status())

    print("Dequeuing jobs:")
    while True:
        job = queue_manager.dequeue()
        if job is None:
            break
        print(f"Dequeued: Job ID: {job.job_id}, User ID: {job.user_id}, Priority: {job.priority}")

    print("Final Queue Status:", queue_manager.get_queue_status())
