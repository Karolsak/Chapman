"""
Main Window for Machine Control Laboratory
Comprehensive GUI with controls and real-time plotting
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DCMotor, InductionMotor, SynchronousMotor
from controllers import PIDController, FOCController, DTCController, VfController
from utils import Simulator


class MachineControlLab:
    """
    Main application window for electrical machine control laboratory
    """

    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Electrical Machine Control Laboratory")
        self.root.geometry("1400x900")

        # Simulation parameters
        self.dt = 0.001  # Time step (1 ms)
        self.update_interval = 50  # GUI update interval (ms)

        # Initialize simulator
        self.simulator = Simulator(dt=self.dt)

        # Initialize motor and controller
        self.motor_type = "DC"
        self.control_type = "PID"
        self.motor = None
        self.controller = None
        self.initialize_motor_and_controller()

        # Control references
        self.speed_ref = 0.0
        self.torque_ref = 0.0
        self.load_torque = 0.0

        # Create GUI
        self.create_widgets()

        # Start simulation loop
        self.running = False
        self.simulation_id = None

    def initialize_motor_and_controller(self):
        """Initialize motor and controller based on selections"""
        # Create motor
        if self.motor_type == "DC":
            self.motor = DCMotor(Ra=0.5, La=0.01, J=0.02, B=0.001, Km=0.5)
            self.motor.Vf = 100  # Field voltage
        elif self.motor_type == "Induction":
            self.motor = InductionMotor(Rs=1.0, Rr=0.8, Ls=0.1, Lr=0.1, Lm=0.09,
                                       J=0.05, B=0.001, poles=4)
        else:  # PMSM
            self.motor = SynchronousMotor(Rs=0.5, Ld=0.005, Lq=0.005,
                                         flux_pm=0.1, J=0.01, B=0.001, poles=4)

        # Create controller
        if self.control_type == "PID":
            self.controller = PIDController(Kp=0.5, Ki=10, Kd=0.001,
                                           output_limits=(-200, 200))
        elif self.control_type == "FOC":
            motor_type_str = "PMSM" if self.motor_type == "PMSM" else "Induction"
            poles = 4
            self.controller = FOCController(motor_type=motor_type_str, poles=poles)
        elif self.control_type == "DTC":
            self.controller = DTCController(flux_ref=0.8, torque_hyst=0.1)
        else:  # V/f
            self.controller = VfController(rated_voltage=380, rated_freq=50)

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Right top - Plots
        plot_frame = ttk.LabelFrame(main_frame, text="Real-Time Plots", padding="10")
        plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Right bottom - Measurements
        measure_frame = ttk.LabelFrame(main_frame, text="Measurements", padding="10")
        measure_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Create control panel widgets
        self.create_control_panel(control_frame)

        # Create plot area
        self.create_plots(plot_frame)

        # Create measurements display
        self.create_measurements(measure_frame)

    def create_control_panel(self, parent):
        """Create control panel with sliders and buttons"""
        row = 0

        # Motor selection
        ttk.Label(parent, text="Motor Type:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.motor_var = tk.StringVar(value="DC")
        motor_frame = ttk.Frame(parent)
        motor_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)

        ttk.Radiobutton(motor_frame, text="DC Motor", variable=self.motor_var,
                       value="DC", command=self.on_motor_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(motor_frame, text="Induction Motor", variable=self.motor_var,
                       value="Induction", command=self.on_motor_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(motor_frame, text="PMSM", variable=self.motor_var,
                       value="PMSM", command=self.on_motor_change).pack(side=tk.LEFT, padx=5)
        row += 1

        # Controller selection
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1

        ttk.Label(parent, text="Control Type:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.control_var = tk.StringVar(value="PID")
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)

        ttk.Radiobutton(control_frame, text="PID", variable=self.control_var,
                       value="PID", command=self.on_control_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="FOC", variable=self.control_var,
                       value="FOC", command=self.on_control_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="DTC", variable=self.control_var,
                       value="DTC", command=self.on_control_change).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="V/f", variable=self.control_var,
                       value="V/f", command=self.on_control_change).pack(side=tk.LEFT, padx=5)
        row += 1

        # Separator
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # Speed control
        ttk.Label(parent, text="Speed Reference (RPM):", font=('Arial', 9, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.speed_ref_var = tk.DoubleVar(value=0)
        speed_slider = ttk.Scale(parent, from_=0, to=3000, orient=tk.HORIZONTAL,
                                variable=self.speed_ref_var, command=self.on_speed_change)
        speed_slider.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1

        self.speed_label = ttk.Label(parent, text="0 RPM")
        self.speed_label.grid(row=row, column=0, columnspan=2, pady=2)
        row += 1

        # Torque control
        ttk.Label(parent, text="Torque Reference (Nm):", font=('Arial', 9, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.torque_ref_var = tk.DoubleVar(value=0)
        torque_slider = ttk.Scale(parent, from_=-50, to=50, orient=tk.HORIZONTAL,
                                 variable=self.torque_ref_var, command=self.on_torque_change)
        torque_slider.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1

        self.torque_label = ttk.Label(parent, text="0.0 Nm")
        self.torque_label.grid(row=row, column=0, columnspan=2, pady=2)
        row += 1

        # Load torque
        ttk.Label(parent, text="Load Torque (Nm):", font=('Arial', 9, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        self.load_var = tk.DoubleVar(value=0)
        load_slider = ttk.Scale(parent, from_=0, to=30, orient=tk.HORIZONTAL,
                               variable=self.load_var, command=self.on_load_change)
        load_slider.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1

        self.load_label = ttk.Label(parent, text="0.0 Nm")
        self.load_label.grid(row=row, column=0, columnspan=2, pady=2)
        row += 1

        # Separator
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # PID Gains (visible when PID selected)
        ttk.Label(parent, text="Controller Gains:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        # Kp
        ttk.Label(parent, text="Kp:").grid(row=row, column=0, sticky=tk.W)
        self.kp_var = tk.DoubleVar(value=0.5)
        kp_slider = ttk.Scale(parent, from_=0, to=10, orient=tk.HORIZONTAL,
                             variable=self.kp_var, command=self.on_gain_change)
        kp_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1

        # Ki
        ttk.Label(parent, text="Ki:").grid(row=row, column=0, sticky=tk.W)
        self.ki_var = tk.DoubleVar(value=10)
        ki_slider = ttk.Scale(parent, from_=0, to=50, orient=tk.HORIZONTAL,
                             variable=self.ki_var, command=self.on_gain_change)
        ki_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1

        # Kd
        ttk.Label(parent, text="Kd:").grid(row=row, column=0, sticky=tk.W)
        self.kd_var = tk.DoubleVar(value=0.001)
        kd_slider = ttk.Scale(parent, from_=0, to=1, orient=tk.HORIZONTAL,
                             variable=self.kd_var, command=self.on_gain_change)
        kd_slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1

        # Separator
        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # Control buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_simulation,
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Reset", command=self.reset_simulation).pack(
            side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Clear Plots", command=self.clear_plots).pack(
            side=tk.LEFT, padx=5)

    def create_plots(self, parent):
        """Create matplotlib plots"""
        # Create figure with subplots
        self.fig = Figure(figsize=(10, 6), dpi=100)

        # Speed plot
        self.ax_speed = self.fig.add_subplot(3, 2, 1)
        self.ax_speed.set_title('Speed (RPM)')
        self.ax_speed.set_xlabel('Time (s)')
        self.ax_speed.grid(True, alpha=0.3)
        self.line_speed, = self.ax_speed.plot([], [], 'b-', label='Actual')
        self.line_speed_ref, = self.ax_speed.plot([], [], 'r--', label='Reference')
        self.ax_speed.legend(loc='upper right')

        # Torque plot
        self.ax_torque = self.fig.add_subplot(3, 2, 2)
        self.ax_torque.set_title('Torque (Nm)')
        self.ax_torque.set_xlabel('Time (s)')
        self.ax_torque.grid(True, alpha=0.3)
        self.line_torque, = self.ax_torque.plot([], [], 'g-', label='Electromagnetic')
        self.ax_torque.legend(loc='upper right')

        # Current plot
        self.ax_current = self.fig.add_subplot(3, 2, 3)
        self.ax_current.set_title('Current (A)')
        self.ax_current.set_xlabel('Time (s)')
        self.ax_current.grid(True, alpha=0.3)
        self.line_current, = self.ax_current.plot([], [], 'm-')

        # Power plot
        self.ax_power = self.fig.add_subplot(3, 2, 4)
        self.ax_power.set_title('Power (W)')
        self.ax_power.set_xlabel('Time (s)')
        self.ax_power.grid(True, alpha=0.3)
        self.line_power, = self.ax_power.plot([], [], 'c-')

        # Efficiency plot
        self.ax_efficiency = self.fig.add_subplot(3, 2, 5)
        self.ax_efficiency.set_title('Efficiency (%)')
        self.ax_efficiency.set_xlabel('Time (s)')
        self.ax_efficiency.set_ylim(0, 100)
        self.ax_efficiency.grid(True, alpha=0.3)
        self.line_efficiency, = self.ax_efficiency.plot([], [], 'orange')

        # Power Factor plot
        self.ax_pf = self.fig.add_subplot(3, 2, 6)
        self.ax_pf.set_title('Power Factor')
        self.ax_pf.set_xlabel('Time (s)')
        self.ax_pf.set_ylim(-1, 1)
        self.ax_pf.grid(True, alpha=0.3)
        self.line_pf, = self.ax_pf.plot([], [], 'brown')

        self.fig.tight_layout()

        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_measurements(self, parent):
        """Create measurements display panel"""
        # Create text widget for measurements
        self.measurements_text = tk.Text(parent, height=8, width=80, font=('Courier', 10))
        self.measurements_text.pack(fill=tk.BOTH, expand=True)

        # Initial text
        self.update_measurements_display({})

    def on_motor_change(self):
        """Handle motor type change"""
        if self.running:
            messagebox.showwarning("Warning", "Stop simulation before changing motor type")
            self.motor_var.set(self.motor_type)
            return

        self.motor_type = self.motor_var.get()
        self.initialize_motor_and_controller()
        self.reset_simulation()

    def on_control_change(self):
        """Handle control type change"""
        if self.running:
            messagebox.showwarning("Warning", "Stop simulation before changing control type")
            self.control_var.set(self.control_type)
            return

        self.control_type = self.control_var.get()
        self.initialize_motor_and_controller()
        self.reset_simulation()

    def on_speed_change(self, value):
        """Handle speed reference change"""
        self.speed_ref = float(value)
        self.speed_label.config(text=f"{self.speed_ref:.0f} RPM")

    def on_torque_change(self, value):
        """Handle torque reference change"""
        self.torque_ref = float(value)
        self.torque_label.config(text=f"{self.torque_ref:.1f} Nm")

    def on_load_change(self, value):
        """Handle load torque change"""
        self.load_torque = float(value)
        self.load_label.config(text=f"{self.load_torque:.1f} Nm")

    def on_gain_change(self, value):
        """Handle controller gain change"""
        if isinstance(self.controller, PIDController):
            self.controller.set_gains(
                Kp=self.kp_var.get(),
                Ki=self.ki_var.get(),
                Kd=self.kd_var.get()
            )

    def start_simulation(self):
        """Start the simulation"""
        self.running = True
        self.simulator.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.run_simulation()

    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.simulator.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.simulation_id is not None:
            self.root.after_cancel(self.simulation_id)

    def reset_simulation(self):
        """Reset the simulation"""
        was_running = self.running
        if was_running:
            self.stop_simulation()

        self.simulator.reset()
        self.initialize_motor_and_controller()
        self.clear_plots()

        if was_running:
            self.start_simulation()

    def clear_plots(self):
        """Clear all plot data"""
        self.line_speed.set_data([], [])
        self.line_speed_ref.set_data([], [])
        self.line_torque.set_data([], [])
        self.line_current.set_data([], [])
        self.line_power.set_data([], [])
        self.line_efficiency.set_data([], [])
        self.line_pf.set_data([], [])

        for ax in [self.ax_speed, self.ax_torque, self.ax_current,
                  self.ax_power, self.ax_efficiency, self.ax_pf]:
            ax.relim()
            ax.autoscale_view()

        self.canvas.draw()

    def run_simulation(self):
        """Main simulation loop"""
        if not self.running:
            return

        # Execute multiple simulation steps per GUI update for performance
        steps_per_update = int(self.update_interval / 1000 / self.dt)

        for _ in range(steps_per_update):
            self.simulation_step()

        # Update GUI
        self.update_plots()

        # Schedule next update
        self.simulation_id = self.root.after(self.update_interval, self.run_simulation)

    def simulation_step(self):
        """Execute one simulation step"""
        # Convert speed reference from RPM to rad/s
        omega_ref = self.speed_ref * 2 * np.pi / 60

        # Apply control based on type and motor
        if self.motor_type == "DC":
            # DC Motor control
            if self.control_type == "PID":
                # Speed control
                Va = self.controller.compute(omega_ref, self.motor.omega, self.dt)
                self.motor.set_inputs(Va=Va, TL=self.load_torque)
            else:
                # Direct voltage control
                Va = 100
                self.motor.set_inputs(Va=Va, TL=self.load_torque)

        elif self.motor_type in ["Induction", "PMSM"]:
            # AC Motor control
            if self.control_type == "PID":
                # Simple PID speed control -> voltage magnitude
                V_mag = self.controller.compute(omega_ref, self.motor.omega, self.dt)
                Vd = V_mag
                Vq = 0
                self.motor.set_inputs(Vd=Vd, Vq=Vq, TL=self.load_torque)

            elif self.control_type == "FOC":
                # Field Oriented Control
                if self.motor_type == "Induction":
                    id_actual = self.motor.isd
                    iq_actual = self.motor.isq
                    theta_e = self.motor.theta_e
                else:  # PMSM
                    id_actual = self.motor.id
                    iq_actual = self.motor.iq
                    theta_e = self.motor.theta_e

                Vd, Vq = self.controller.compute(omega_ref, self.motor.omega,
                                                id_actual, iq_actual, theta_e, self.dt)
                self.motor.set_inputs(Vd=Vd, Vq=Vq, TL=self.load_torque)

            elif self.control_type == "V/f":
                # V/f Control
                freq, voltage, omega_e = self.controller.compute_closed_loop(
                    self.speed_ref, self.motor.omega, 4, self.dt)

                # Convert to dq voltages (simplified)
                Vd = voltage / np.sqrt(2)
                Vq = 0
                self.motor.set_inputs(Vd=Vd, Vq=Vq, TL=self.load_torque, omega_e=omega_e)

        # Step motor
        measurements = self.motor.step(self.dt)

        # Log data
        references = {
            'speed_ref': self.speed_ref,
            'torque_ref': self.torque_ref
        }
        self.simulator.step(measurements, references)

        # Update measurements display periodically
        if int(self.simulator.time * 1000) % 100 == 0:
            self.update_measurements_display(measurements)

    def update_measurements_display(self, measurements):
        """Update measurements text display"""
        self.measurements_text.delete(1.0, tk.END)

        text = "=== REAL-TIME MEASUREMENTS ===\n\n"

        if measurements:
            text += f"Speed:       {measurements.get('speed_rpm', 0):8.1f} RPM\n"
            text += f"Torque:      {measurements.get('Te', 0):8.3f} Nm\n"

            if 'Is' in measurements:
                text += f"Current:     {measurements.get('Is', 0):8.3f} A\n"
            elif 'ia' in measurements:
                text += f"Current:     {abs(measurements.get('ia', 0)):8.3f} A\n"

            text += f"Power:       {measurements.get('Pout', 0):8.1f} W\n"
            text += f"Efficiency:  {measurements.get('efficiency', 0):8.1f} %\n"
            text += f"Power Factor:{measurements.get('pf', 0):8.3f}\n"

            if self.motor_type == "Induction":
                text += f"Slip:        {measurements.get('slip', 0)*100:8.3f} %\n"

        else:
            text += "No data available\n"

        text += f"\nSimulation Time: {self.simulator.time:.3f} s"

        self.measurements_text.insert(1.0, text)

    def update_plots(self):
        """Update all plots with latest data"""
        history = self.simulator.get_history(num_points=2000)

        if len(history.get('time', [])) < 2:
            return

        time = history['time']

        # Update speed plot
        self.line_speed.set_data(time, history['speed'])
        self.line_speed_ref.set_data(time, history['speed_ref'])
        self.ax_speed.relim()
        self.ax_speed.autoscale_view()

        # Update torque plot
        self.line_torque.set_data(time, history['torque'])
        self.ax_torque.relim()
        self.ax_torque.autoscale_view()

        # Update current plot
        self.line_current.set_data(time, history['current'])
        self.ax_current.relim()
        self.ax_current.autoscale_view()

        # Update power plot
        self.line_power.set_data(time, history['power'])
        self.ax_power.relim()
        self.ax_power.autoscale_view()

        # Update efficiency plot
        self.line_efficiency.set_data(time, history['efficiency'])
        self.ax_efficiency.relim()
        self.ax_efficiency.autoscale_view()

        # Update power factor plot
        self.line_pf.set_data(time, history['pf'])
        self.ax_pf.relim()
        self.ax_pf.autoscale_view()

        # Redraw canvas
        self.canvas.draw_idle()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MachineControlLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
