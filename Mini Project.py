import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
 
# ─────────────────────────────────────────────
#  Performance logic (unchanged from original)
# ─────────────────────────────────────────────
class Performance:
    def __init__(self, Runs, Balls):
        self.runs = Runs
        self.balls = Balls
 
    def Total(self):
        return sum(self.runs)
 
    def Total_balls(self):
        return sum(self.balls)
 
    def Total_Strike_rate(self):
        tb = self.Total_balls()
        if tb == 0:
            return 0
        return (self.Total() / tb) * 100
 
    def innings_strike_rates(self):
        sr_list = []
        for r, b in zip(self.runs, self.balls):
            sr_list.append(0 if b == 0 else (r / b) * 100)
        return sr_list
 
 
# ─────────────────────────────────────────────
#  Tkinter Application
# ─────────────────────────────────────────────
class CricketApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏏 Cricket Performance Tracker")
        self.configure(bg="#1a1a2e")
        self.resizable(False, False)
 
        self.NUM_INNINGS = 5
        self.runs_entries = []
        self.balls_entries = []
 
        self._build_ui()
 
    # ── UI Construction ──────────────────────
    def _build_ui(self):
        # Title
        tk.Label(
            self,
            text="🏏 Cricket Performance Tracker",
            font=("Georgia", 18, "bold"),
            bg="#1a1a2e", fg="#e2b96f"
        ).grid(row=0, column=0, columnspan=4, pady=(18, 8))
 
        # Column headers
        headers = ["Innings", "Runs Scored", "Balls Faced"]
        for col, h in enumerate(headers):
            tk.Label(
                self, text=h,
                font=("Courier", 11, "bold"),
                bg="#1a1a2e", fg="#a0c4ff", width=14
            ).grid(row=1, column=col, padx=10, pady=4)
 
        # Input rows
        for i in range(self.NUM_INNINGS):
            tk.Label(
                self, text=f"Innings {i + 1}",
                font=("Courier", 10),
                bg="#1a1a2e", fg="#ffffff", width=14
            ).grid(row=i + 2, column=0, padx=10, pady=5)
 
            r_entry = self._make_entry()
            r_entry.grid(row=i + 2, column=1, padx=10, pady=5)
            self.runs_entries.append(r_entry)
 
            b_entry = self._make_entry()
            b_entry.grid(row=i + 2, column=2, padx=10, pady=5)
            self.balls_entries.append(b_entry)
 
        # Buttons
        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.grid(row=self.NUM_INNINGS + 2, column=0, columnspan=4, pady=14)
 
        self._make_button(btn_frame, "Calculate & Plot", self._calculate, "#e2b96f", "#1a1a2e").pack(side="left", padx=8)
        self._make_button(btn_frame, "Clear", self._clear, "#ff6b6b", "#1a1a2e").pack(side="left", padx=8)
 
        # Summary labels
        self.summary_frame = tk.Frame(self, bg="#16213e", bd=1, relief="groove")
        self.summary_frame.grid(row=self.NUM_INNINGS + 3, column=0, columnspan=4, padx=20, pady=(0, 12), sticky="ew")
        self.summary_labels = {}
        fields = ["Total Runs", "Total Balls", "Overall Strike Rate"]
        for i, f in enumerate(fields):
            tk.Label(self.summary_frame, text=f"{f}:", font=("Courier", 10, "bold"),
                     bg="#16213e", fg="#a0c4ff", width=20, anchor="e"
                     ).grid(row=i, column=0, pady=3, padx=(10, 4))
            lbl = tk.Label(self.summary_frame, text="—", font=("Courier", 10),
                           bg="#16213e", fg="#e2b96f", width=14, anchor="w")
            lbl.grid(row=i, column=1, pady=3)
            self.summary_labels[f] = lbl
 
        # Chart area
        self.fig, self.ax = plt.subplots(figsize=(6, 3), facecolor="#1a1a2e")
        self.fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.18)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(
            row=self.NUM_INNINGS + 4, column=0, columnspan=4, padx=20, pady=(0, 20)
        )
        self._draw_empty_chart()
 
    def _make_entry(self):
        e = tk.Entry(
            self, width=12, font=("Courier", 11),
            bg="#16213e", fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat", bd=4, justify="center"
        )
        return e
 
    def _make_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent, text=text, command=command,
            font=("Courier", 11, "bold"),
            bg=bg, fg=fg, activebackground="#c9a04e",
            relief="flat", padx=16, pady=6, cursor="hand2"
        )
 
    # ── Actions ──────────────────────────────
    def _calculate(self):
        runs_list, balls_list = [], []
 
        for i in range(self.NUM_INNINGS):
            r_val = self.runs_entries[i].get().strip()
            b_val = self.balls_entries[i].get().strip()
 
            if not r_val or not b_val:
                messagebox.showerror("Missing Input", f"Please fill in all fields for Innings {i + 1}.")
                return
            if not r_val.isdigit() or not b_val.isdigit():
                messagebox.showerror("Invalid Input", f"Innings {i + 1}: Enter whole numbers only.")
                return
 
            runs_list.append(int(r_val))
            balls_list.append(int(b_val))
 
        perf = Performance(runs_list, balls_list)
        sr_list = perf.innings_strike_rates()
 
        # Update summary
        self.summary_labels["Total Runs"].config(text=str(perf.Total()))
        self.summary_labels["Total Balls"].config(text=str(perf.Total_balls()))
        self.summary_labels["Overall Strike Rate"].config(text=f"{perf.Total_Strike_rate():.2f}")
 
        # Update chart
        self._draw_chart(sr_list)
 
    def _clear(self):
        for e in self.runs_entries + self.balls_entries:
            e.delete(0, tk.END)
        for lbl in self.summary_labels.values():
            lbl.config(text="—")
        self._draw_empty_chart()
 
    # ── Chart helpers ─────────────────────────
    def _draw_empty_chart(self):
        self.ax.clear()
        self.ax.set_facecolor("#16213e")
        self.ax.set_title("Innings-wise Strike Rate", color="#e2b96f", fontsize=11, pad=8)
        self.ax.set_xlabel("Innings", color="#a0c4ff")
        self.ax.set_ylabel("Strike Rate", color="#a0c4ff")
        self.ax.tick_params(colors="#aaaaaa")
        for spine in self.ax.spines.values():
            spine.set_edgecolor("#444466")
        self.ax.grid(color="#2a2a4a", linestyle="--", linewidth=0.7)
        self.canvas.draw()
 
    def _draw_chart(self, sr_list):
        self.ax.clear()
        self.ax.set_facecolor("#16213e")
 
        innings = list(range(1, self.NUM_INNINGS + 1))
        self.ax.plot(innings, sr_list, color="#e2b96f", linewidth=2.5,
                     marker="o", markersize=7, markerfacecolor="#ff6b6b")
 
        for x, y in zip(innings, sr_list):
            self.ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                             xytext=(0, 10), ha="center", color="#ffffff", fontsize=8)
 
        self.ax.set_title("Innings-wise Strike Rate", color="#e2b96f", fontsize=11, pad=8)
        self.ax.set_xlabel("Innings", color="#a0c4ff")
        self.ax.set_ylabel("Strike Rate", color="#a0c4ff")
        self.ax.set_xticks(innings)
        self.ax.tick_params(colors="#aaaaaa")
        for spine in self.ax.spines.values():
            spine.set_edgecolor("#444466")
        self.ax.grid(color="#2a2a4a", linestyle="--", linewidth=0.7)
        self.canvas.draw()
 
 
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = CricketApp()
    app.mainloop()