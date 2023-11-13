from random import randint
from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np


class PreemptivePriorityScheduling: # Class for simulating Preemptive Priority CPU Scheduling
    process_list = [] # List to Store the Processes [PID, AT, BT, RT, PL,CT]
    WT = 0
    TT = 0
    def inputUser(self, no_of_processes): # USER INPUT
        for process_id in range(1, no_of_processes + 1): # Loop to enter user values for each process
            temporary = [] # Temporary list to store values
            
            while True:
                arrival_time = int(input(f"\nEnter Arrival Time for P{process_id}: ")) # Arrival Time input
                
                if [pr for pr in self.process_list if pr[1] == arrival_time]: # Arrival Time duplicate checker
                    print("Duplicate")
                else:
                    break

            burst_time = int(input(f"Enter Burst Time for P{process_id}: ")) # Burst Time input
            
            remaining_time = deepcopy(burst_time) # Remaining Time is used for the scheduling process to simulate the remaining burst time of the process

            priority_level = int(input(f"Enter Priority Level for P{process_id}: ")) # Priority Level input
            
            completion_time = 0 # Completion Time is the time that the process finished running

            temporary = [f"P{process_id}", arrival_time, burst_time, remaining_time, priority_level, completion_time] # Storing input values inside a list
            
            self.process_list.append(temporary) # Appending the list of values inside the list of processes
        
    def inputRandom(self, no_of_processes): # RANDOM INPUT
        half = no_of_processes // 2 
        randomizer_limit = no_of_processes + half # Randomizer limit is 150% of the Number of Processes
        
        for process_id in range(1, no_of_processes + 1): # Loop to enter random values for each process
            temporary = [] 

            while True:
                arrival_time = randint(0, randomizer_limit)
                
                if [pr for pr in self.process_list if pr[1] == arrival_time]:
                    pass
                else:
                    break

            burst_time = randint(1, randomizer_limit)
            
            remaining_time = deepcopy(burst_time)

            priority_level = randint(1, no_of_processes)
            
            completion_time = 0

            temporary = [f"P{process_id}", arrival_time, burst_time, remaining_time, priority_level, completion_time]
            
            self.process_list.append(temporary)

        
    def schedulingProcess(self): # Scheduling Algorithm
        # Print input table
        print("\nProcess\tArrival Time\tBurst Time\tPriority Level")
        for process in self.process_list:
            print(f"{process[0]}\t{process[1]}\t\t{process[2]}\t\t{process[4]}")
        
        current_time = 0 # Current Time Frame
        completed_list = [] # List for completed processes
        ready_queue = [] # Memory Queue
         # this is a 2 dimensional array in which [0] is the process name [1] service time [2] execution stop time
        cur_process_data = {}
        flag = True
        temp = None
        counter = 0
        while len(completed_list) < len(self.process_list): # Loop for the Algorithm
            for process in self.process_list:
                if process[1] <= current_time and process not in completed_list and process not in ready_queue: # Inserting newly arrived processes to the Memory Queue
                    ready_queue.append(process)
            
            print(f"\nTimeframe {current_time}")
            print(ready_queue)
            if not ready_queue: # Checking for idle time
                print(f"Running: None")
                current_time += 1
                continue # Skip rest of the algorithm if idle time
            
            ready_queue.sort(key=lambda x: x[4]) # Sorting the ready queue based on Priority Level
            
            current_process = ready_queue[0] # Set current process as process with highest level in memory queue
            
            current_process[3] -= 1 # Decerement current process bust time
            if flag:
                cur_process_data[counter] = []
                cur_process_data[counter].append(current_process[0])
                cur_process_data[counter].append(current_time)
                temp = current_process[0]
                flag = False
            elif temp != current_process[0]:
                counter += 1
                cur_process_data[counter-1].append(current_time)
                flag = True
            
            # Print Simulation
            print(f"Running: {current_process[0]}")
            print(f"Current Burst Time: {current_process[3]}")
            print(f"Priority Level: {current_process[4]}")
            
            if current_process[3] == 0: # Check if process is Completed
                completed_list.append(current_process) # Append current process to completed list
                ready_queue.pop(0) # Remove current process from ready queue
                current_process[5] = current_time + 1 # Set completion time for current process
            
            current_time += 1 # Increment Current Time Frame


        cur_process_data[counter].append(current_time)
        print(cur_process_data)
        # Initialize Totals of TT and WT
        total_wt = 0
        total_tt = 0
        
        for process in self.process_list: # Loop to calculate WT and TT of each rocess
            turnaround_time = process[5] - process[1] # Calculate TT of process (Completion Time - Arrival Time)
            waiting_time = turnaround_time - process[2] # Calculate WT of process (Turnaround Time - Burst Time)
            
            total_wt += waiting_time # Add TT of the process to the total
            total_tt += turnaround_time # Add WT of the process to the total
        
        # Compute Averages
        self.WT = total_wt / len(self.process_list)
        self.TT = total_tt / len(self.process_list)
        
        

        return cur_process_data

    def plot_gantt_chart(self, cur_process_data):
        fig, gnt = plt.subplots()
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Processes')

        try:
            colors = plt.cm.viridis(np.linspace(0, 1, len(cur_process_data)))

            for i, (key, value) in enumerate(cur_process_data.items()):
                process_name = value[0]
                start_time = value[1]
                end_time = value[2]

                # Use a different color for each process
                color = colors[i]

                gnt.broken_barh([(start_time, end_time - start_time)], (0, 1), facecolors=(color))

                # Add process labels
                gnt.text(start_time + 1, 1, process_name, verticalalignment='center', horizontalalignment='center', color='black')

            plt.show()
        except:
            plt.show()


# Main Machinery
proseso = PreemptivePriorityScheduling() # Create instance

process_amount = int(input("Enter # of Processes: ")) # Input # of Processes

user_or_random = input("User or Random Input? [U/R]: ") # Select if User or Random Values

if user_or_random.lower() == "u":
    proseso.inputUser(process_amount)
elif user_or_random.lower() == "r":
    proseso.inputRandom(process_amount)
    
cur = proseso.schedulingProcess() # Run Scheduling Algotihm
proseso.plot_gantt_chart(cur)