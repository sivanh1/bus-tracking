import random
import time
import csv
import datetime
import threading
import queue
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from geopy.distance import geodesic

# --------------------------
# Global Configuration and Variables
# --------------------------
TOTAL_SEATS = 40           # Total capacity of the bus
occupied_seats = 0         # Global variable tracking the current passenger count

# Define bus stops with sample GPS coordinates (latitude, longitude)
bus_stops = [
    ("Stop A", (37.7749, -122.4194)),
    ("Stop B", (37.7760, -122.4170)),
    ("Stop C", (37.7770, -122.4150)),
    ("Stop D", (37.7780, -122.4130)),
    ("Stop E", (37.7790, -122.4110))
]

# Generate a predefined bus route by interpolating between stops
route_points = []
points_per_segment = 20  # More points yield a smoother route
for i in range(len(bus_stops) - 1):
    start_stop = bus_stops[i][1]
    end_stop = bus_stops[i+1][1]
    for t in range(points_per_segment):
        factor = t / points_per_segment
        lat = start_stop[0] + (end_stop[0] - start_stop[0]) * factor
        lon = start_stop[1] + (end_stop[1] - start_stop[1]) * factor
        route_points.append((lat, lon))
route_points.append(bus_stops[-1][1])  # Ensure final stop is included

# Queues for simulation state updates and for alert messages
simulation_queue = queue.Queue()
alerts_queue = queue.Queue()

# --------------------------
# Simulation Function (runs in a separate thread)
# --------------------------
def simulation_loop():
    global occupied_seats
    current_index = 0
    simulation_steps = len(route_points)
    
    # Open CSV file for logging
    csv_filename = "bus_simulation_log.csv"
    csvfile = open(csv_filename, "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp", "lat", "lon", "stop_name", "seat_occupied", "alert"])
    
    while True:
        curr_point = route_points[current_index]
        alert_message = ""
        current_stop = ""
        
        # Simulate route deviation with 5% probability
        if random.random() < 0.05:
            deviation_lat = random.uniform(0.0005, 0.002)
            deviation_lon = random.uniform(0.0005, 0.002)
            curr_point = (curr_point[0] + deviation_lat, curr_point[1] + deviation_lon)
            alert_message = "Route Deviation!"
            print(alert_message)
        
        # Check if current point is near any bus stop (within 50 meters)
        for stop in bus_stops:
            stop_name, stop_coord = stop
            distance = geodesic(curr_point, stop_coord).meters
            if distance < 50:
                current_stop = stop_name
                if not alert_message:
                    alert_message = f"Stop Arrived: {stop_name}"
                # Simulate boarding and alighting events
                boarding = random.randint(0, 5)
                alighting = random.randint(0, 3)
                occupied_seats = max(0, min(TOTAL_SEATS, occupied_seats + boarding - alighting))
                print(f"{stop_name}: Boarding {boarding}, Alighting {alighting}, Occupancy: {occupied_seats}/{TOTAL_SEATS}")
                break  # Process only one stop event per loop
        
        # Check if bus has reached full capacity
        if occupied_seats >= TOTAL_SEATS:
            alert_message = "Bus Full!"
            print(alert_message)
        
        # Compose simulation state update
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state_update = {
            "timestamp": timestamp,
            "curr_point": curr_point,
            "occupied_seats": occupied_seats,
            "stop": current_stop,
            "alert": alert_message
        }
        simulation_queue.put(state_update)
        
        # Log to CSV
        writer.writerow([timestamp, curr_point[0], curr_point[1], current_stop, occupied_seats, alert_message])
        csvfile.flush()
        
        # If an alert occurred, add it to alerts queue
        if alert_message:
            alerts_queue.put((timestamp, alert_message))
        
        current_index = (current_index + 1) % simulation_steps
        time.sleep(0.2)

    # (In case of KeyboardInterrupt, CSV file will be closed in a real application.)
    csvfile.close()

# --------------------------
# Main Tkinter Application with Embedded Matplotlib and Kanban Board
# --------------------------
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Bus Tracking System")
        self.geometry("1200x700")
        
        # Create two main frames: left for simulation plot, right for Kanban board
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.kanban_frame = tk.Frame(self)
        self.kanban_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_plot()         # Embed Matplotlib figure for simulation visualization
        self.create_kanban_board() # Build Kanban board UI for alerts
        
        # Start periodic updates from simulation and alerts queues
        self.update_simulation_plot()
        self.update_alerts()
    
    def create_plot(self):
        # Create a Matplotlib figure with two subplots (bus map and seat occupancy)
        self.fig, (self.ax_map, self.ax_seat) = plt.subplots(1, 2, figsize=(8, 6))
        self.fig.tight_layout()
        
        # Plot the full route on the map
        route_lats = [pt[0] for pt in route_points]
        route_lons = [pt[1] for pt in route_points]
        self.ax_map.plot(route_lons, route_lats, 'k--', label="Route")
        
        # Mark bus stops on the map
        for stop in bus_stops:
            stop_name, (lat, lon) = stop
            self.ax_map.plot(lon, lat, 'bo', markersize=6)
            self.ax_map.text(lon + 0.0002, lat + 0.0002, stop_name, fontsize=9)
        self.ax_map.set_xlabel("Longitude")
        self.ax_map.set_ylabel("Latitude")
        self.ax_map.set_title("Bus Location Tracking")
        self.ax_map.legend()
        
        # Create an initial bus marker (empty)
        self.bus_marker, = self.ax_map.plot([], [], 'ro', markersize=10, label="Bus")
        
        # Set up the seat occupancy chart (initial state)
        self.seat_labels = ["Occupied", "Available"]
        self.ax_seat.bar(self.seat_labels, [occupied_seats, TOTAL_SEATS - occupied_seats],
                         color=["red", "green"])
        self.ax_seat.set_ylim(0, TOTAL_SEATS + 5)
        self.ax_seat.set_title("Seat Occupancy")
        
        # Embed the Matplotlib figure into Tkinter via FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_simulation_plot(self):
        # Poll simulation_queue and update the Matplotlib plots accordingly
        try:
            while True:
                state = simulation_queue.get_nowait()
                curr_point = state["curr_point"]
                occupied = state["occupied_seats"]
                
                # Update the bus marker (x-data: longitude, y-data: latitude)
                self.bus_marker.set_data([curr_point[1]], [curr_point[0]])
                
                # Update the seat occupancy bar chart
                self.ax_seat.cla()  # Clear the axis
                self.ax_seat.bar(self.seat_labels, [occupied, TOTAL_SEATS - occupied], 
                                 color=["red", "green"])
                self.ax_seat.set_ylim(0, TOTAL_SEATS + 5)
                self.ax_seat.set_title("Seat Occupancy")
        except queue.Empty:
            pass
        
        # Redraw the canvas to display the updates
        self.canvas.draw_idle()
        self.after(100, self.update_simulation_plot)
    
    def create_kanban_board(self):
        # Build a basic Kanban board with two columns: Alerts and Resolved
        self.alerts_container = tk.LabelFrame(self.kanban_frame, text="Alerts", padx=10, pady=10)
        self.resolved_container = tk.LabelFrame(self.kanban_frame, text="Resolved", padx=10, pady=10)
        self.alerts_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.resolved_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Set up a canvas with scrollbar for alerts
        self.alerts_canvas = tk.Canvas(self.alerts_container)
        self.alerts_scrollbar = tk.Scrollbar(self.alerts_container, orient="vertical",
                                             command=self.alerts_canvas.yview)
        self.alerts_inner = tk.Frame(self.alerts_canvas)
        self.alerts_inner.bind("<Configure>", lambda e: self.alerts_canvas.configure(
            scrollregion=self.alerts_canvas.bbox("all")))
        self.alerts_canvas.create_window((0, 0), window=self.alerts_inner, anchor="nw")
        self.alerts_canvas.configure(yscrollcommand=self.alerts_scrollbar.set)
        self.alerts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.alerts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Resolved alerts inner frame
        self.resolved_inner = tk.Frame(self.resolved_container)
        self.resolved_inner.pack(fill=tk.BOTH, expand=True)
        
        # A dictionary to store alert cards keyed by timestamp
        self.alert_cards = {}
    
    def update_alerts(self):
        # Poll the alerts_queue for new alerts and add them as cards
        try:
            while True:
                timestamp, message = alerts_queue.get_nowait()
                self.add_alert_card(timestamp, message)
        except queue.Empty:
            pass
        self.after(1000, self.update_alerts)
    
    def add_alert_card(self, timestamp, message):
        # Create an alert card with a Resolve button
        card_frame = tk.Frame(self.alerts_inner, relief=tk.RIDGE, bd=2, padx=5, pady=5)
        card_frame.pack(fill=tk.X, pady=2)
        alert_text = f"{timestamp}\n{message}"
        label = tk.Label(card_frame, text=alert_text, justify=tk.LEFT)
        label.pack(side=tk.LEFT, padx=5)
        resolve_button = tk.Button(card_frame, text="Resolve",
                                   command=lambda: self.mark_resolved(card_frame, alert_text))
        resolve_button.pack(side=tk.RIGHT, padx=5)
        self.alert_cards[timestamp] = card_frame
    
    def mark_resolved(self, card, alert_text):
        # Move the alert card to the Resolved column and modify its style
        card.pack_forget()
        card.config(relief=tk.SUNKEN, bg="#d3ffd3")
        for widget in card.winfo_children():
            widget.destroy()
        card_label = tk.Label(card, text=f"{alert_text}\n[Resolved]", justify=tk.LEFT, fg="gray")
        card_label.pack(side=tk.LEFT, padx=5)
        card.pack(in_=self.resolved_inner, fill=tk.X, pady=2)

if __name__ == "__main__":
    # Start the simulation thread
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()
    
    # Launch the main Tkinter application (which embeds the plot and Kanban board)
    app = MainApp()
    app.mainloop()
