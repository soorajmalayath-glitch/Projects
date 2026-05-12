#Player Performance Analyzer (last 5 matches)


class Performance:
    def __init__(self,Runs,Balls):
        self.runs=Runs
        self.balls=Balls
    
    def Total(self):
        sum=0
        for r in self.runs:
            sum+=r
        return sum
    def Total_balls(self):
        sum=0
        for b in self.balls:
            sum+=b
        return sum
    def Total_Strike_rate(self):
        avg=(self.Total()/self.Total_balls())*100
        return avg
    
    def innings_strike_rates(self):
        sr_list = []
        for r, b in zip(self.runs, self.balls):
            if b == 0:
                sr_list.append(0)
            else:
                sr_list.append((r / b) * 100)
        return sr_list


    def display(self):
        print(f"Runs scored:",self.runs)
        print(f"Balls played:",self.balls)
        print(f"Total Runs Scored:",self.Total())
        print(f"Total Balls faced:",self.Total_balls())
        print(f"Total Strike rate:",self.Total_Strike_rate())
        print(f"The innings wise Strike Rate:",self.innings_strike_rates())



runs_list=[]
balls_list=[]

for i in range(5):
    Runs=int(input("Enter the runs scored"))
    Balls=int(input("Enter the Balls faced"))
    runs_list.append(Runs)
    balls_list.append(Balls)
    


Play=Performance(Runs,Balls)
Play=Performance(runs_list,balls_list)
Play.display()

import matplotlib.pyplot as plt
from tkinter import messagebox

sr_list = Play.innings_strike_rates()


innings = [1, 2, 3, 4, 5]

plt.plot(innings, sr_list)

plt.title("Innings-wise Strike Rate")
plt.xlabel("Innings")
plt.ylabel("Strike Rate")

plt.grid()
plt.show()

import tkinter as tk

root = tk.Tk()
root.title("Player Performance Analyzer")

runs_entries = []
balls_entries = []

# Create input fields
for i in range(5):
    tk.Label(root, text=f"Innings {i+1} Runs").grid(row=i, column=0)
    run_entry = tk.Entry(root)
    run_entry.grid(row=i, column=1)
    runs_entries.append(run_entry)

    tk.Label(root, text=f"Innings {i+1} Balls").grid(row=i, column=2)
    ball_entry = tk.Entry(root)
    ball_entry.grid(row=i, column=3)
    balls_entries.append(ball_entry)


def calculate():
    try:
        runs_list = [int(e.get()) for e in runs_entries]
        balls_list = [int(e.get()) for e in balls_entries]

        Play = Performance(runs_list, balls_list)

        # Show results in GUI
        result_text.set(
            f"Total Runs: {Play.Total()}\n"
            f"Total Balls: {Play.Total_balls()}\n"
            f"Strike Rate: {round(Play.Total_Strike_rate(),2)}\n"
            f"Innings SR: {Play.innings_strike_rates()}"
        )

        # Plot graph
        sr_list = Play.innings_strike_rates()
        innings = [1,2,3,4,5]

        plt.plot(innings, sr_list)
        plt.title("Innings-wise Strike Rate")
        plt.xlabel("Innings")
        plt.ylabel("Strike Rate")
        plt.grid()
        plt.show()

    except:
        messagebox.showerror("Error", "Please enter valid numbers")


# Button
tk.Button(root, text="Calculate Performance", command=calculate).grid(row=6, column=1)

# Result display
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text).grid(row=7, column=0, columnspan=4)

root.mainloop()


