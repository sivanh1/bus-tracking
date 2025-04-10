# Smart Bus Tracking System

This project simulates an IoT-based smart bus tracking and seat monitoring system using Python. The application provides real-time simulation, visualization, and alert management with the following features:

- **Real-Time Simulation & Visualization**
  - The bus follows a predefined route with embedded GPS coordinates.
  - Boarding and alighting events are randomly simulated.
  - An embedded Matplotlib plot (within the Tkinter UI) displays the bus route, current location, and a live bar chart for seat occupancy.

- **Kanban Board for Alerts**
  - Alerts such as "Route Deviation", "Stop Arrived", and "Bus Full!" are generated during the simulation.
  - These alerts are presented in a Kanban-style UI where you can mark alerts as resolved.

- **CSV Data Logging**
  - Every simulation update (timestamp, bus location, stop information, seat occupancy, and alert messages) is logged into a CSV file (`bus_simulation_log.csv`) for further analysis.

## Folder Structure

Since this version is implemented as a single file, your project folder may contain:


> **Note:**  
> This version is self-contained in the `main.py` file, which embeds the Matplotlib visualization into the Tkinter UI.

## Prerequisites

Ensure you have Python 3.x installed along with the following packages:

- [Matplotlib](https://matplotlib.org)
- [Geopy](https://geopy.readthedocs.io)

You can install the dependencies with:

```bash
pip install matplotlib geopy

```
# Bus Simulation Application

This project simulates a bus traversing a predefined route with real-time visualization and an integrated Kanban board UI for managing alerts. The application utilizes Tkinter for the UI, Matplotlib for visualization, and a background simulation loop to generate dynamic events and logging.

## Running the Application

1. **Open a Terminal or Command Prompt**  
   Navigate to the project folder.

2. **Execute the following command:**
   ```bash
   python main.py


This application simulates a bus moving along a predefined route with real-time visualization and event logging. The interface is divided into two main sections: the simulation visualization panel and the Kanban board for alerts management.

## Table of Contents

- [Application Overview](#application-overview)
  - [Simulation Visualization (Left Side)](#simulation-visualization-left-side)
  - [Kanban Board UI (Right Side)](#kanban-board-ui-right-side)
- [How It Works](#how-it-works)
  - [Simulation Loop](#simulation-loop)
  - [Embedded Visualization](#embedded-visualization)
  - [Kanban Board Features](#kanban-board-features)
  - [Data Logging](#data-logging)
- [Customization & Extensions](#customization--extensions)
- [Running the Application](#running-the-application)
- [Additional Notes](#additional-notes)

## Application Overview

### Simulation Visualization (Left Side)

- **Map View:**  
  - An embedded Matplotlib figure displays the bus route.
  - Bus stops along the route are clearly marked.
  - A red marker on the map represents the current location of the bus.

- **Seat Occupancy:**  
  - A real-time bar chart shows the number of occupied versus available seats on the bus.
  - This chart updates as boarding and alighting events occur.

### Kanban Board UI (Right Side)

- **Alerts:**  
  - Alerts generated during the simulation are displayed as individual cards in the "Alerts" column.

- **Resolve Alerts:**  
  - Each alert card includes a **Resolve** button.
  - Clicking the button moves the alert from the "Alerts" column to the "Resolved" column.

## How It Works

### Simulation Loop

- **Background Thread:**  
  - The simulation loop runs in a background thread and simulates the bus moving along a predefined route.

- **Passenger Events:**  
  - The simulation includes boarding and alighting events at bus stops.

- **Data Logging:**  
  - All simulation events are continuously logged.
  - The log is saved as `bus_simulation_log.csv` in the project folder.

- **Queue Updates:**  
  - State updates and alert messages are posted to thread-safe queues from the simulation loop.

### Embedded Visualization

- **Matplotlib Integration:**  
  - The Matplotlib figure is embedded into the Tkinter UI using `FigureCanvasTkAgg`.

- **Real-Time Updates:**  
  - The simulation queue is polled periodically to update:
    - The bus marker on the map.
    - The seat occupancy bar chart.

### Kanban Board Features

- **Alert Display:**  
  - The Kanban board polls an alert queue to display new alerts in the "Alerts" column.

- **Resolve Functionality:**  
  - Alerts can be marked as “Resolved” by clicking a dedicated **Resolve** button.
  - This transfers the alert from the "Alerts" column to the "Resolved" column.

### Data Logging

- All simulation data is continuously logged and appended to the `bus_simulation_log.csv` file.
- This provides a detailed record of all simulation events for troubleshooting and review.

## Customization & Extensions

### Route & Stops

- Modify the simulation route by updating the `bus_stops` list in the `main.py` file.
- Change the GPS coordinates to simulate different routes or scenarios.

### Simulation Settings

- **Points per Segment:**  
  - Adjust the `points_per_segment` parameter to change the route's resolution.

- **Event Probabilities:**  
  - Fine-tune the probabilities for:
    - Route deviations.
    - Passenger boarding events.
    - Passenger alighting events.
  
- These settings can be customized to simulate various scenarios with different complexities.

### User Interface Customization

- **Tkinter UI:**  
  - The Kanban board and visualization panels can be extended and styled.
  - Use Tkinter widget options to adjust layouts, fonts, and colors.

- **Matplotlib Configuration:**  
  - Customize the embedded charts using Matplotlib’s configuration options.
  - Modify axis labels, markers, and other chart properties to suit your needs.

## Running the Application

1. **Install Dependencies:**  
   Ensure you have Python installed along with the required libraries:
   ```bash
   pip install matplotlib tkinter

