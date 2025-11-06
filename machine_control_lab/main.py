#!/usr/bin/env python3
"""
Electrical Machine Control Laboratory
Main entry point for the application

Author: Machine Control Laboratory Team
Description: Comprehensive laboratory for modeling, simulation, and development
             of advanced control systems for electrical machines.

Features:
- DC Motor, Induction Motor, and PMSM models
- PID, FOC, DTC, and V/f control strategies
- Real-time simulation and visualization
- Interactive parameter adjustment via sliders
- Speed, torque, and power factor control
"""

import tkinter as tk
from gui.main_window import MachineControlLab


def main():
    """Main application entry point"""
    # Create root window
    root = tk.Tk()

    # Create and run application
    app = MachineControlLab(root)

    # Start GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
