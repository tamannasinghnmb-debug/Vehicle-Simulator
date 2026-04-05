# Vehicle Stopping Simulator



import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ----------------- CONFIG -----------------
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"
TEXT_COLOR = "#000000"
GRAPH_COLOR_DISTANCE = "blue"
GRAPH_COLOR_VELOCITY = "red"
GRAPH_COLOR_ACCEL = "green"
FONT_STYLE = ("Arial", 12)
# ------------------------------------------

# Coefficients of friction for roads
road_friction = {
    "Dry": 0.7,
    "Wet": 0.4,
    "Icy": 0.1
}

# Vehicle data: mass (kg) for models
vehicles = {
    "Scooty": {"Honda Activa": 110, "TVS Jupiter": 115},
    "Car": {"Maruti Swift": 950, "Hyundai i20": 1000},
    "Bike": {"KTM Duke": 180, "Royal Enfield": 200},
    "Tempo": {"Tempo Traveller": 2200},
    "Bus": {"Volvo Bus": 12000},
    "Truck": {"Tata Truck": 8000}
}

g = 9.8  # Gravity

# ----------------- APP -----------------
class VehicleSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Stopping Simulator")
        self.root.config(bg=BG_COLOR)
        self.root.geometry("800x700")
        self.user_choices = {}
        self.create_road_choice()
    
    # ---------- Road Choice ----------
    def create_road_choice(self):
        self.clear_frame()
        tk.Label(self.root, text="Choose Road Type", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_STYLE).pack(pady=10)
        for road in road_friction:
            tk.Button(self.root, text=road, bg=BUTTON_COLOR, font=FONT_STYLE,
                      command=lambda r=road: self.select_road(r)).pack(pady=5)
    
    def select_road(self, road):
        self.user_choices["road"] = road
        self.create_vehicle_type_choice()
    
    # ---------- Vehicle Type ----------
    def create_vehicle_type_choice(self):
        self.clear_frame()
        tk.Label(self.root, text="Choose Vehicle Type", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_STYLE).pack(pady=10)
        for vtype in vehicles:
            tk.Button(self.root, text=vtype, bg=BUTTON_COLOR, font=FONT_STYLE,
                      command=lambda v=vtype: self.select_vehicle_type(v)).pack(pady=5)
    
    def select_vehicle_type(self, vtype):
        self.user_choices["vehicle_type"] = vtype
        self.create_vehicle_model_choice(vtype)
    
    # ---------- Vehicle Model ----------
    def create_vehicle_model_choice(self, vtype):
        self.clear_frame()
        tk.Label(self.root, text="Choose Vehicle Model", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_STYLE).pack(pady=10)
        for model in vehicles[vtype]:
            tk.Button(self.root, text=model, bg=BUTTON_COLOR, font=FONT_STYLE,
                      command=lambda m=model: self.select_model(m)).pack(pady=5)
    
    def select_model(self, model):
        self.user_choices["model"] = model
        self.user_choices["mass"] = vehicles[self.user_choices["vehicle_type"]][model]
        self.create_velocity_input()
    
    # ---------- Velocity Input ----------
    def create_velocity_input(self):
        self.clear_frame()
        tk.Label(self.root, text="Enter Initial Velocity (m/s)", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_STYLE).pack(pady=10)
        self.velocity_entry = tk.Entry(self.root, font=FONT_STYLE)
        self.velocity_entry.pack(pady=5)
        tk.Button(self.root, text="Calculate & Show Graphs", bg=BUTTON_COLOR, font=FONT_STYLE, command=self.calculate_stopping).pack(pady=10)
        
        # Create matplotlib figure for multiple graphs
        self.fig, self.axs = plt.subplots(3, 1, figsize=(6,10))
        self.axs[0].set_title("Distance vs Time")
        self.axs[1].set_title("Velocity vs Time")
        self.axs[2].set_title("Acceleration vs Time")
        for ax in self.axs:
            ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)
    
    # ---------- Calculation ----------
    def calculate_stopping(self):
        try:
            v0 = float(self.velocity_entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid number!")
            return
        
        mass = self.user_choices["mass"]
        friction = road_friction[self.user_choices["road"]]
        
        stopping_force = friction * mass * g  # in N
        deceleration = stopping_force / mass  # in m/s²
        stopping_time = v0 / deceleration
        stopping_distance = (v0**2) / (2*deceleration)
        
        messagebox.showinfo("Results", 
                            f"Stopping Force: {stopping_force:.2f} N\n"
                            f"Deceleration: {deceleration:.2f} m/s²\n"
                            f"Stopping Distance: {stopping_distance:.2f} m\n"
                            f"Stopping Time: {stopping_time:.2f} s")
        
        # Prepare data for graphs
        t_vals = np.linspace(0, stopping_time, 100)
        v_vals = v0 - deceleration * t_vals
        x_vals = v0 * t_vals - 0.5 * deceleration * t_vals**2
        a_vals = np.full_like(t_vals, -deceleration)
        
        # Clear previous plots
        for ax in self.axs:
            ax.clear()
        
        # Distance vs Time
        self.axs[0].plot(t_vals, x_vals, color=GRAPH_COLOR_DISTANCE)
        self.axs[0].set_xlabel("Time (s)")
        self.axs[0].set_ylabel("Distance (m)")
        self.axs[0].set_title("Distance vs Time")
        self.axs[0].grid(True)
        
        # Velocity vs Time
        self.axs[1].plot(t_vals, v_vals, color=GRAPH_COLOR_VELOCITY)
        self.axs[1].set_xlabel("Time (s)")
        self.axs[1].set_ylabel("Velocity (m/s)")
        self.axs[1].set_title("Velocity vs Time")
        self.axs[1].grid(True)
        
        # Acceleration vs Time
        self.axs[2].plot(t_vals, a_vals, color=GRAPH_COLOR_ACCEL)
        self.axs[2].set_xlabel("Time (s)")
        self.axs[2].set_ylabel("Acceleration (m/s²)")
        self.axs[2].set_title("Acceleration vs Time")
        self.axs[2].grid(True)
        
        self.canvas.draw()
    
    # ---------- Helper ----------
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run App
root = tk.Tk()
app = VehicleSimulator(root)
root.mainloop()

