import customtkinter, math
from NonPreemptivePriorityScheduling import _NonPreemptivePriorityScheduling
from PreemptivePriorityScheduling import _PreemptivePriorityScheduling
import PreemptivePriorityScheduling
from matplotlib import pyplot as plt
from matplotlib.table import Table
import tkinter as tk
from tkinter import ttk
from PIL import Image

## TODO
# Make the labels at the center
# 

NP = 0
data = []
WT = 0
TT = 0
class ProcessTableBox(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        # Label For Process Table
        title = customtkinter.CTkLabel(self, text="Process Table", fg_color="transparent", font=("Arial", 20))
        title.pack()
        # # The Table generated by Matplotlib that shows the process
        # # this inlucdes the Process ID, Burst Time, Arrival Time and Priority Number

        processtable = ttk.Treeview(self, columns=("Process ID", "Arrival Time", "Burst Time", "Priority Number"), show="headings", height=NP)
        processtable.heading("Process ID", text="Process ID")
        processtable.heading("Arrival Time", text="Arrival Time")
        processtable.heading("Burst Time", text="Burst Time")
        processtable.heading("Priority Number", text="Priority Number")
        processtable.pack()

        global data
        # Insert data into the table
        for element in data:
            processtable.insert("", "end", values=(element[0], element[1], element[2], element[3]))
            


class GanttChartBox(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.height = 4000
        global NP
        global WT
        global TT
        if NP > 30 and NP <= 50:
            self.height = 1500
        elif NP <= 30 and NP >= 20:
            self.height = 1000
        elif NP < 20:
            self.height = 500       

        result = "Result dd"
        # Label for GANTT Chart
        self.title = customtkinter.CTkLabel(self, text=f"GANTT Chart({title})", fg_color="transparent", font=("Arial", 20))
        self.title.pack()

        ## WT Avg
        self.title = customtkinter.CTkLabel(self, text=f"Waiting Time Average: {round(WT, 2)}", fg_color="transparent", font=("Arial", 13))
        self.title.pack()
        
        ## TT Avg
        self.title = customtkinter.CTkLabel(self, text=f"Turnaround Time Average: {round(TT, 2)}", fg_color="transparent", font=("Arial", 13))
        self.title.pack()
        
        self.myimg = customtkinter.CTkImage(Image.open("./GANTT_OUTPUT/GTChart.png"), size=(600, self.height))
        self.imgLabel = customtkinter.CTkLabel(self, image=self.myimg, text="")
        self.imgLabel.pack()


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, title):
        super().__init__()
        self.geometry("1080x720")
        # Back button for TOP_LEVEL WINDOW
        self.back_Btn = customtkinter.CTkButton(self, text="Back to Main", command=self.backToMain)
        self.back_Btn.pack()
        # Instantiating Process Table Frame
        self.Process_Table_Box = ProcessTableBox(self)
        self.Process_Table_Box.pack(side=customtkinter.LEFT, expand=True, fill=customtkinter.BOTH)
        # Instantiating Process 
        self.Gantt_Chart_Box = GanttChartBox(self, title)
        self.Gantt_Chart_Box.pack(side=customtkinter.RIGHT, expand=True, fill=customtkinter.BOTH)
        

    def backToMain(self):
        global data
        global WT
        global TT
        global NP

        data = []
        WT = 0
        TT = 0
        NP = 0
        self.destroy()

class OptionWindow(customtkinter.CTkFrame): # Amo adi an window kun hain naka butang an mga buttons
    def __init__(self, master):
        super().__init__(master)
        ## Instatiating the _Non-Preemptive Priority Scheduling Class
        self.NonPPS_Instance = _NonPreemptivePriorityScheduling()
        self.PPS_Instance = _PreemptivePriorityScheduling()
        
        #Burst Time Slider
        self.BTLabel = customtkinter.CTkLabel(self, text="Unsay Max Burst Time imo gusto", fg_color="transparent")
        self.BTLabel.grid(row=0, column=0)
        self.Burst_Time = customtkinter.CTkSlider(self, from_=1, to=15, command=self.setBT, number_of_steps=15)
        self.Burst_Time.grid(row=1, column=0, padx=10, pady=10)
        self.BTSlider_CurValue = customtkinter.CTkLabel(self, text=math.trunc(self.Burst_Time.get()), fg_color="transparent", width=20)
        self.BTSlider_CurValue.grid(row=1, column=1)
        
        #Input Box for Number of Processes
        self.Process_InputLabel = customtkinter.CTkLabel(self, text="Pila kabuok imo Processes")
        self.Process_InputLabel.grid(row=0, column=2)
        self.Process_Input = customtkinter.CTkEntry(self, placeholder_text="Number of Processes", width=190)
        self.Process_Input.grid(row=1, column=2, padx=10, pady=10)

        # What Algorithm to Use
        self.AlgoChoice = customtkinter.CTkLabel(self, text="Unsay nga algorithm gamiton bai?", fg_color="transparent")
        self.AlgoChoice.grid(row=0, column=3)
        self.AlgoMenu = customtkinter.CTkOptionMenu(self, values=["Preemptive Priority Scheduling", "Non-Preemtive Priotity Scheduling"], 
        width=250)
        self.AlgoMenu.grid(row=1, column=3)

        # Start Button
        self.start_Btn = customtkinter.CTkButton(self, text="Pagsugod", command=self.startExecution)
        self.start_Btn.grid(row=1, column=4, padx=10, pady=10)
        

    def setBT(self, value):
        self.BTSlider_CurValue.configure(text=math.trunc(value))
    

    
    def GenerateGANTT_Chart(self, processList, process_Timing):
        fig, ax = plt.subplots()
        for i, (process, timings) in enumerate(process_Timing.items()):
            start, end = timings
            ax.barh(i, end - start, left=start, align='center', label=process)

        ax.set_xlabel('Time', fontsize=9)
        ax.set_yticks(range(len(process_Timing)))
        ax.set_yticklabels(process_Timing.keys(), fontsize=7)

        plt.grid(axis='x')
        plt.savefig("./GANTT_OUTPUT/GTChart.png", bbox_inches='tight', dpi=100)
    

    def startExecution(self):
        global NP
        global WT
        global TT
        
        NP = int(self.Process_Input.get())
        if self.AlgoMenu.get() == "Preemptive Priority Scheduling":
            
            processList = self.PPS_Instance.inputRandom(int(self.Process_Input.get()), math.trunc(self.Burst_Time.get()))
            PreemptivePriorityScheduling.runner(processList)
            TT = PreemptivePriorityScheduling.TT
            WT = PreemptivePriorityScheduling.WT
            
           
        elif self.AlgoMenu.get() == "Non-Preemtive Priotity Scheduling":
            processList = self.NonPPS_Instance.Random_Input(int(self.Process_Input.get()), math.trunc(self.Burst_Time.get()))
            processTiming = self.NonPPS_Instance.Execute(processList)
            WT = self.NonPPS_Instance.waitingTime
            TT = self.NonPPS_Instance.turnaroundTime
            
            self.GenerateGANTT_Chart(processList, processTiming)
        
        ## The two lines below are used sa printing of process table
        global data
        data = processList

        ## This Generates the Top Level window that shows the charts and Table
        self.toplev = ToplevelWindow(self.AlgoMenu.get())

    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
      
        self.title("CPU Scheduler Algorithm")
        self.geometry("1000x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        ## Welcome Label
        self.greet = customtkinter.CTkLabel(self, text="CPU Algorithm Simulator", fg_color="transparent", font=("Arial", 40))
        self.greet.grid(row=0, column=0, sticky="ew")

        # ## Member Names
        # ## Ivan
        # self.greet = customtkinter.CTkLabel(self, text="Galang, John Ivan", fg_color="transparent", font=("Arial", 20))
        # self.greet.grid(row=1, column=0, sticky="ew")
        # ## Michael
        # self.greet = customtkinter.CTkLabel(self, text="Ochengco, Michael Angelo", fg_color="transparent", font=("Arial", 20))
        # self.greet.grid(row=2, column=0, sticky="ew")
        # # Shawn
        # self.greet = customtkinter.CTkLabel(self, text="Sudaria, Shawn Michael", fg_color="transparent", font=("Arial", 20))
        # self.greet.grid(row=3, column=0, sticky="ew")

        ### OPTION MENU
        self.optionMenu = OptionWindow(self)
        self.optionMenu.grid(row=4, column=0, sticky="ew", columnspan=2, padx=50, pady=10)

app = App()
app.mainloop()
