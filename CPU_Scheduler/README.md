# CPU Scheduling Algorithm Simulator

This is a Python-based simulator for CPU scheduling algorithms, featuring Non-Preemptive Priority Scheduling and Preemptive Priority Scheduling. The simulator generates random processes with arrival times, burst times, and priority levels, executes the scheduling algorithms, and visualizes the results using Gantt charts.

## Files

> The Original code structure of this project looked like this before being packaged in an windows PE file.

### 1. `main.py`

This is the main script that launches the GUI for the simulator. It uses the `customtkinter` library for creating the graphical interface. The main functionalities include inputting the number of processes, selecting the scheduling algorithm, and displaying the Gantt chart and process table.

### 2. `NonPreemptivePriorityScheduling.py`

Contains the implementation of the Non-Preemptive Priority Scheduling algorithm. It generates random input processes, executes the scheduling, and calculates waiting time and turnaround time.

### 3. `PreemptivePriorityScheduling.py`

Implements the Preemptive Priority Scheduling algorithm. It generates random input processes, executes the scheduling, and calculates waiting time and turnaround time. Additionally, it includes a Gantt chart plotting function.

## Usage

1. Run `CPU_Malware.exe` inside the dist folder to start the GUI. Don't mind the filename😁
2. Input the number of processes and select the scheduling algorithm.
3. Click the "Start" button to execute the simulation.
4. The Gantt chart and process table will be displayed in a new window.

## Dependencies

-   `customtkinter`: A custom-themed tkinter library.
-   `matplotlib`: Used for plotting Gantt charts.
-   `PIL`: Python Imaging Library for image processing.

## Contributors

-   John Ivan Galang
-   Michael Angelo Ochengco
-   Shawn Michael Sudaria

Feel free to contribute or open issues!
