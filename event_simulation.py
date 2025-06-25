# task5_event_simulation.py

import time
import random
import threading
from dataclasses import dataclass
from queue import Queue
from typing import List, Optional, Dict


# ================== Job Data Class ===============
@dataclass
class Job:
    user_id: str
    job_id: str
    priority: int
    timestamp: float
    waiting_time: float = 0.0


# ================== Concurrent Job Queue ==================
class ConcurrentQueueManager:
    def __init__(self, capacity: int):
        self.queue = Queue(maxsize=capacity)
        self.lock = threading.Lock()
        self.capacity = capacity
        self.job_counter = 0

    def generate_job_id(self) -> str:
        with self.lock:
            self.job_counter += 1
            return f"JOB-{self.job_counter:04d}"

    def enqueue(self, user_id: str, priority: int, job_obj: Job = None) -> Optional[Job]:
        with self.lock:
            if self.queue.full():
                return None

            if job_obj:
                self.queue.put(job_obj)
                return job_obj

            job = Job(
                user_id=user_id,
                job_id=self.generate_job_id(),
                priority=priority,
                timestamp=time.time()
            )
            self.queue.put(job)
            return job

    def dequeue(self) -> Optional[Job]:
        with self.lock:
            if self.queue.empty():
                return None
            return self.queue.get()

    def process_simultaneous_submissions(self, submissions: List[tuple[str, int]]) -> List[Optional[Job]]:
        threads = []
        results = []

        def submit(user_id, priority):
            job = self.enqueue(user_id, priority)
            results.append(job)

        for user_id, priority in submissions:
            t = threading.Thread(target=submit, args=(user_id, priority))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results

    def get_queue_status(self) -> Dict:
        with self.lock:
            return {
                "size": self.queue.qsize(),
                "is_empty": self.queue.empty(),
                "is_full": self.queue.full(),
                "capacity": self.capacity
            }


# ================== Priority Queue Stub ==================
class PriorityQueue:
    def __init__(self):
        pass  # In this task, aging is done manually within EventSimulator


# ================== Job Expiry Manager ==================
class JobExpiryManager:
    def __init__(self, expiry_time: int):
        self.expiry_time = expiry_time  # in seconds


# ================== Queue Visualizer ==================
class QueueVisualizer:
    @staticmethod
    def display_queue_status(status: Dict):
        print("\n--- Queue Status ---")
        print(f"Size: {status['size']}/{status['capacity']}")
        print(f"Is Empty: {'Yes' if status['is_empty'] else 'No'}")
        print(f"Is Full: {'Yes' if status['is_full'] else 'No'}")
        print("---------------------")


# ================== Task 5: Event Simulator ==================
class EventSimulator:
    def __init__(
        self,
        queue_manager: ConcurrentQueueManager,
        expiry_manager: JobExpiryManager,
        visualizer: QueueVisualizer,
        aging_interval: int = 5,
        tick_duration: float = 1.0
    ):
        self.queue_manager = queue_manager
        self.expiry_manager = expiry_manager
        self.visualizer = visualizer
        self.aging_interval = aging_interval
        self.tick_duration = tick_duration
        self.tick_count = 0

    def tick(self):
        self.tick_count += 1
        current_time = time.time()
        print(f"\n=== TICK {self.tick_count} ===")

        jobs: List[Job] = []

        # Dequeue all jobs
        while not self.queue_manager.queue.empty():
            job = self.queue_manager.dequeue()
            if job:
                job.waiting_time = current_time - job.timestamp
                jobs.append(job)

        active_jobs = []
        for job in jobs:
            # Apply priority aging
            if job.waiting_time >= self.aging_interval:
                old_priority = job.priority
                job.priority = min(job.priority + 1, 10)
                if job.priority > old_priority:
                    print(f"[AGING] {job.job_id}: Priority {old_priority} → {job.priority}")

            # Expiry check
            if job.waiting_time >= self.expiry_manager.expiry_time:
                print(f"[EXPIRED] {job.job_id}: Removed after {job.waiting_time:.1f}s")
            else:
                active_jobs.append(job)

        # Reinsert active jobs
        for job in active_jobs:
            self.queue_manager.enqueue(job.user_id, job.priority, job_obj=job)

        # Show queue status
        self.visualizer.display_queue_status(self.queue_manager.get_queue_status())

    def simulate(self, ticks: int):
        for _ in range(ticks):
            self.tick()
            time.sleep(self.tick_duration)


# ================== Test/Demo Run ==================
def run_task5_demo():
    print("=== Task 5: Event Simulation Demo ===")

    capacity = 5
    expiry_time = 10
    aging_interval = 5

    queue_manager = ConcurrentQueueManager(capacity)
    expiry_manager = JobExpiryManager(expiry_time)
    visualizer = QueueVisualizer()

    # Submit 5 jobs at random priority
    submissions = [(f"USER-{i+1}", random.randint(1, 3)) for i in range(capacity)]
    queue_manager.process_simultaneous_submissions(submissions)

    # Run simulation
    simulator = EventSimulator(
        queue_manager,
        expiry_manager,
        visualizer,
        aging_interval=aging_interval,
        tick_duration=1.0
    )

    simulator.simulate(ticks=5)


if __name__ == "__main__":
    run_task5_demo()
