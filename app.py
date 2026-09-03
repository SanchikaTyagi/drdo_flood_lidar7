"""
Main Application Entry Point for DRDO Defense & Disaster Perception System.
"""
import sys
import tkinter as tk
from mission.mission_controller import MissionController
from visualization.live_dashboard import LiveTacticalDashboard

def main():
    root = tk.Tk()
    controller = MissionController()
    app = LiveTacticalDashboard(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
