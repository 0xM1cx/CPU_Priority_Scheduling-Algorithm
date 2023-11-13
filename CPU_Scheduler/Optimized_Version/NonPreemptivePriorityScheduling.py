from random import randint, seed
from copy import deepcopy

class _NonPreemptivePriorityScheduling:
    processList = []
    process_Timing = {}
    waitingTime = 0
    turnaroundTime = 0

    def __init__(self, seed_value=None):
        if seed_value is not None:
            seed(seed_value)

    def Random_Input(self, num_processes, max_burst):
        half = num_processes // 2
        randomizer_limit = num_processes + half

        for process_id in range(1, num_processes + 1):
            while True:
                arrival_time = randint(0, randomizer_limit)
                if not any(_process[1] == arrival_time for _process in self.processList):
                    break

            burst_time = randint(1, max_burst)
            priority = randint(1, num_processes)

            self.processList.append([f"P{process_id}", arrival_time, burst_time, priority])

        return self.processList

    def Execute(self, process_list):
        current_time = 0
        process_complete = []
        memory_queue = []

        while len(process_complete) < len(self.processList):
            for process in self.processList:
                if process[1] <= current_time and process not in process_complete and process not in memory_queue:
                    memory_queue.append(process)

            if not memory_queue:
                current_time += 1
                continue

            memory_queue.sort(key=lambda x: (x[3], x[1]))

            current_process = memory_queue.pop(0)
            process_complete.append(current_process)
            self.process_Timing[current_process[0]] = (current_time, current_time + current_process[2])
            current_time += current_process[2]

        total_waiting_time = 0
        total_turnaround_time = 0

        for process in self.processList:
            turnaround_time = current_time - process[1]
            waiting_time = turnaround_time - process[2]

            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time

        self.waitingTime = total_waiting_time / len(self.processList)
        self.turnaroundTime = total_turnaround_time / len(self.processList)

        return self.process_Timing
