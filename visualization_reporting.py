class QueueVisualizer:
    @staticmethod
    def display_queue_status(status: Dict):
        print("\n=== Queue Status ===")
        print(f"Size: {status['size']}/{status['capacity']}")
        print(f"Jobs in queue: {'Yes' if not status['is_empty'] else 'No'}")
        print(f"Queue full: {'Yes' if status['is_full'] else 'No'}")

    @staticmethod
    def display_job(job: Job):
        print(f"Job ID: {job.job_id}")
        print(f"User: {job.user_id}, Priority: {job.priority}")
        print(f"Waiting time: {job.waiting_time:.2f}s")