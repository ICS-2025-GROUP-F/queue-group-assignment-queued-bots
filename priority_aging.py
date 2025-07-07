def apply_priority_aging(self, aging_interval, max_priority=10):
    if self.is_empty():
        return

    # Extract active jobs in current queue order
    jobs = []
    index = self.head
    for _ in range(self.size):
        job = self.queue[index]
        if job:
            if job.waiting_time >= aging_interval and job.priority < max_priority:
                old_priority = job.priority
                job.priority += 1
                print(f"[AGING] Job {job.job_id} from User {job.user_id} aged: {old_priority} → {job.priority}")
            jobs.append(job)
        index = (index + 1) % self.capacity

    # Sort the jobs: highest priority first, then longest waiting
    jobs.sort(key=lambda j: (-j.priority, -j.waiting_time))

    # Restor the queue after sorting
    self.queue = [None] * self.capacity
    self.head = 0
    self.tail = -1
    self.size = 0
    for job in jobs:
        self.enqueue_job(job.user_id, job.job_id, job.priority)
        # Restore waiting time (since enqueue resets it)
        self.queue[self.tail].waiting_time = job.waiting_time


