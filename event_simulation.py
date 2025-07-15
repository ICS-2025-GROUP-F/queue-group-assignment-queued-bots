def tick(self):
    self.current_tick += 1
    print(f"\n[Tick {self.current_tick}]")


    for job in self.queue:
        job['waiting_time'] += 1


    self.apply_priority_aging()


    self.remove_expired_jobs()

   
    self.show_status()
