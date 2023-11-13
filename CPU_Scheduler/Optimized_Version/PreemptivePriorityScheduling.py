from random import randint, seed
from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np 
import os

class _PreemptivePriorityScheduling:
    process_list = []
    four_column_process_list = []
    WT = 0
    TT = 0

    def __init__(self, seed_value=None):
        process_list = []
        four_column_process_list = []
        WT = 0
        TT = 0 
        if seed_value is not None:
            seed(seed_value)

    def inputRandom(self, no_of_processes, max_burst):
        half = no_of_processes // 2
        randomizer_limit = no_of_processes + half

        for process_id in range(1, no_of_processes + 1):
            while True:
                arrival_time = randint(0, randomizer_limit)

                if not any(pr[1] == arrival_time for pr in self.process_list):
                    break

            burst_time = randint(1, max_burst)
            remaining_time = deepcopy(burst_time)
            priority_level = randint(1, no_of_processes)
            completion_time = 0

            temporary = [f"P{process_id}", arrival_time, burst_time, remaining_time, priority_level, completion_time]

            self.process_list.append(temporary)
            self.four_column_process_list.append([f"P{process_id}", arrival_time, burst_time, priority_level])

        return self.four_column_process_list

    def schedulingProcess(self):
        current_time = 0
        completed_list = []
        ready_queue = []
        cur_process_data = {}
        flag = True
        temp = None
        counter = 0

        while len(completed_list) < len(self.process_list):
            for process in self.process_list:
                if process[1] <= current_time and process not in completed_list and process not in ready_queue:
                    ready_queue.append(process)

            if not ready_queue:
                current_time += 1
                continue

            ready_queue.sort(key=lambda x: x[4])

            current_process = ready_queue[0]
            current_process[3] -= 1

            if flag:
                cur_process_data[counter] = []
                cur_process_data[counter].append(current_process[0])
                cur_process_data[counter].append(current_time)
                temp = current_process[0]
                flag = False
            elif temp != current_process[0]:
                counter += 1
                cur_process_data[counter - 1].append(current_time)
                flag = True

            if current_process[3] == 0:
                completed_list.append(current_process)
                ready_queue.pop(0)
                current_process[5] = current_time + 1

            current_time += 1

        last_process = list(cur_process_data.keys())[-1]
        cur_process_data[last_process].append(current_time)

        total_wt = 0
        total_tt = 0

        for process in self.process_list:
            turnaround_time = process[5] - process[1]
            waiting_time = turnaround_time - process[2]

            total_wt += waiting_time
            total_tt += turnaround_time

        self.TT = total_wt / len(self.process_list)
        self.WT = total_tt / len(self.process_list)
        return cur_process_data

    def plot_gantt_chart(self, cur_process_data):
        fig, gnt = plt.subplots()
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Processes')


        colors = plt.cm.viridis(np.linspace(0, 1, len(cur_process_data)))
        
        for i, (key, value) in enumerate(cur_process_data.items()):
            process_name = value[0]
            start_time = value[1]
            end_time = value[2]

            color = colors[i]
            gnt.broken_barh([(start_time, end_time - start_time)], (0, 1), facecolors=(color))

            gnt.text(start_time + 1, 1, process_name, verticalalignment='center', horizontalalignment='center', color='black')
        plt.savefig("GTChart.png", bbox_inches='tight', dpi=150)
    





def runner(process_list):
    proseso = _PreemptivePriorityScheduling()
    cur = proseso.schedulingProcess()
    proseso.plot_gantt_chart(cur)
    return proseso.TT, proseso.WT

