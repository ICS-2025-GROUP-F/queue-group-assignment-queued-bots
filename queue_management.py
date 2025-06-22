class Job:
    # Job together with its attributes 

    def __init__(self, user_id, job_id, priority):
        self.user_id = user_id
        self.job_id = job_id
        self.priority = priority
        self.waiting_time = 0  

    def __repr__(self):
        return f"Job({self.user_id}, {self.job_id}, Priority={self.priority}, WaitingTime={self.waiting_time})"


class QueueManager:
    # Jobs managed in circular queue structure
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = -1
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue_job(self, user_id, job_id, priority):
        if self.is_full():
            raise OverflowError("Cannot enqueue new job.")
        self.tail = (self.tail + 1) % self.capacity
        self.queue[self.tail] = Job(user_id, job_id, priority)
        self.size += 1

    def dequeue_job(self):
        if self.is_empty():
            return None
        job = self.queue[self.head]
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return job

    def show_status(self):
        if self.is_empty():
            print("The queue is empty.")
            return []
        jobs = []
        index = self.head
        for i in range(self.size):
            jobs.append(self.queue[index])
            index = (index + 1) % self.capacity
        return jobs


