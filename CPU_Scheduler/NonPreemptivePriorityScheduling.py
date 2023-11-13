from random import randint
from time import sleep
from os import system

# This is a Non-Preemtive Priotity Scheduling Program
# Round Robin nak nabutang kay ambot, wa ko na ayusa kay bayn maruba 
class _NonPreemptivePriorityScheduling:

    processList = []
    process_Timing = {}
    waitingTime = 0
    turnaroundTime = 0
    
    # Function that generates random input for processes
    def Random_Input(self, Num_Process, Max_Burst):
        half = Num_Process // 2
        randomizer_limit = Num_Process + half
        
        for IDprocess in range(1, Num_Process + 1):
            tempList = []

            while True:
                arrivalTime = randint(0, randomizer_limit)
                if [_process for _process in self.processList if _process[1] == arrivalTime]:
                    pass
                else:   
                    break

            burstTime = randint(1, Max_Burst)
            Priority = randint(1, Num_Process)
            
            tempList = [f"P{IDprocess}", arrivalTime, burstTime, Priority]

            self.processList.append(tempList)
        
        return self.processList

    # Execution of the Algorithm
    def Execute(self, processList):
        currentTime = 0
        ProcessComplete = []
        MemoryQueue = []
        while len(ProcessComplete) < len(self.processList):
            for process in self.processList:
                if process[1] <= currentTime and process not in ProcessComplete and process not in MemoryQueue:
                    MemoryQueue.append(process)

            # Executed if there is no Process in the moment
            if not MemoryQueue:
                currentTime += 1
                continue

            MemoryQueue.sort(key=lambda x: (x[3], x[1]))  # Sort by priority and arrival time
            
            current_process = MemoryQueue.pop(0) # pops the first elemnt stored in the memory queue
            ProcessComplete.append(current_process)
            self.process_Timing[current_process[0]] = (currentTime, currentTime+current_process[2])
            currentTime += current_process[2]



        totalWT = 0
        totalTT = 0

        for process in self.processList:
            turnarroundTime = currentTime - process[1]
            waitingTime = turnarroundTime - process[2]

            totalWT += waitingTime
            totalTT += turnarroundTime

        WT = totalWT / len(self.processList) # Waiting time
        TT = totalTT / len(self.processList) # Turnaround TIme

        
        self.waitingTime = WT
        self.turnaroundTime =  TT

        return self.process_Timing
