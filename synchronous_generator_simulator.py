#!/usr/bin/env python3
"""
Three-Phase Synchronous Generator Dynamic Simulator
Solves synchronous generator problems with dynamic ODE simulation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import math

class SynchronousGeneratorSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Three-Phase Synchronous Generator Dynamic Simulator")
        self.root.geometry("1400x900")

        # Problem parameters
        self.S_base = 200e6  # 200 MVA
        self.V_base_LL = 16e3  # 16 kV line-line
        self.V_base_phase = self.V_base_LL / np.sqrt(3)
        self.I_base = self.S_base / (np.sqrt(3) * self.V_base_LL)  # Should be 7.217 kA
        self.Z_base = self.V_base_LL**2 / self.S_base

        # Default values (all in per-unit unless specified)
        self.Xs_pu = tk.DoubleVar(value=1.60)
        self.V_terminal_kV = tk.DoubleVar(value=15.0)
        self.E_initial_kV = tk.DoubleVar(value=24.0)
        self.delta_initial_deg = tk.DoubleVar(value=25.0)

        # Dynamic simulation parameters
        self.Pm_pu = tk.DoubleVar(value=0.8)  # Mechanical power input
        self.H = tk.DoubleVar(value=3.5)  # Inertia constant (seconds)
        self.D = tk.DoubleVar(value=0.05)  # Damping coefficient
        self.solver_type = tk.StringVar(value="RK45")

        # Simulation time control
        self.sim_time = tk.DoubleVar(value=5.0)
        self.time_step = tk.DoubleVar(value=0.01)

        # Animation control
        self.is_running = False
        self.animation_id = None
        self.current_time = 0.0
        self.sim_data = None

        # Results storage
        self.results = {}

        # Setup GUI
        self.setup_gui()

        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)

        # Initial calculation
        self.calculate_all()

    def setup_gui(self):
        """Setup the GUI layout"""
        # Main container with grid
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure root grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Parameters & Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.setup_controls(control_frame)

        # Right top panel - Results
        results_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding="10")
        results_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.results_text = tk.Text(results_frame, height=15, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        # Right bottom panel - Plots
        plot_frame = ttk.LabelFrame(main_frame, text="Dynamic Visualization", padding="10")
        plot_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)

        self.setup_plots(plot_frame)

    def setup_controls(self, parent):
        """Setup control sliders and buttons"""
        row = 0

        # Generator Parameters
        ttk.Label(parent, text="Generator Parameters", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        # Synchronous Reactance
        ttk.Label(parent, text="Xs (p.u.):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=0.5, to=3.0, orient=tk.HORIZONTAL,
                          variable=self.Xs_pu, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(parent, textvariable=tk.StringVar(value=f"{self.Xs_pu.get():.2f}")).grid(row=row, column=2)
        self.Xs_label = ttk.Label(parent, text=f"{self.Xs_pu.get():.2f}")
        self.Xs_label.grid(row=row, column=2)
        row += 1

        # Terminal Voltage
        ttk.Label(parent, text="V terminal (kV):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=10.0, to=20.0, orient=tk.HORIZONTAL,
                          variable=self.V_terminal_kV, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.V_label = ttk.Label(parent, text=f"{self.V_terminal_kV.get():.2f}")
        self.V_label.grid(row=row, column=2)
        row += 1

        # Internal EMF
        ttk.Label(parent, text="E internal (kV):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=15.0, to=35.0, orient=tk.HORIZONTAL,
                          variable=self.E_initial_kV, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.E_label = ttk.Label(parent, text=f"{self.E_initial_kV.get():.2f}")
        self.E_label.grid(row=row, column=2)
        row += 1

        # Power Angle
        ttk.Label(parent, text="δ angle (deg):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=0.0, to=90.0, orient=tk.HORIZONTAL,
                          variable=self.delta_initial_deg, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.delta_label = ttk.Label(parent, text=f"{self.delta_initial_deg.get():.2f}")
        self.delta_label.grid(row=row, column=2)
        row += 1

        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # Dynamic Simulation Parameters
        ttk.Label(parent, text="Dynamic Simulation", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        # Mechanical Power
        ttk.Label(parent, text="Pm (p.u.):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=0.0, to=2.0, orient=tk.HORIZONTAL,
                          variable=self.Pm_pu, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.Pm_label = ttk.Label(parent, text=f"{self.Pm_pu.get():.2f}")
        self.Pm_label.grid(row=row, column=2)
        row += 1

        # Inertia Constant
        ttk.Label(parent, text="H (seconds):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=1.0, to=10.0, orient=tk.HORIZONTAL,
                          variable=self.H, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.H_label = ttk.Label(parent, text=f"{self.H.get():.2f}")
        self.H_label.grid(row=row, column=2)
        row += 1

        # Damping Coefficient
        ttk.Label(parent, text="D (damping):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=0.0, to=0.5, orient=tk.HORIZONTAL,
                          variable=self.D, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.D_label = ttk.Label(parent, text=f"{self.D.get():.3f}")
        self.D_label.grid(row=row, column=2)
        row += 1

        # Simulation Time
        ttk.Label(parent, text="Sim time (s):").grid(row=row, column=0, sticky=tk.W)
        slider = ttk.Scale(parent, from_=1.0, to=20.0, orient=tk.HORIZONTAL,
                          variable=self.sim_time, command=lambda x: self.update_from_slider())
        slider.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        self.sim_time_label = ttk.Label(parent, text=f"{self.sim_time.get():.1f}")
        self.sim_time_label.grid(row=row, column=2)
        row += 1

        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # Solver Selection
        ttk.Label(parent, text="ODE Solver:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W)
        row += 1

        solver_frame = ttk.Frame(parent)
        solver_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        ttk.Radiobutton(solver_frame, text="RK45 (Runge-Kutta)", variable=self.solver_type,
                       value="RK45").pack(anchor=tk.W)
        ttk.Radiobutton(solver_frame, text="Euler", variable=self.solver_type,
                       value="Euler").pack(anchor=tk.W)
        row += 1

        ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1

        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="Calculate All", command=self.calculate_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation).pack(side=tk.LEFT, padx=5)
        self.anim_button = ttk.Button(button_frame, text="Start Animation", command=self.toggle_animation)
        self.anim_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_parameters).pack(side=tk.LEFT, padx=5)

    def setup_plots(self, parent):
        """Setup matplotlib plots"""
        self.fig = Figure(figsize=(10, 8), dpi=100)

        # Create subplots
        self.ax1 = self.fig.add_subplot(2, 2, 1)  # Power-Angle curve
        self.ax2 = self.fig.add_subplot(2, 2, 2)  # Phasor diagram
        self.ax3 = self.fig.add_subplot(2, 2, 3)  # Delta vs time
        self.ax4 = self.fig.add_subplot(2, 2, 4)  # Speed vs time

        self.fig.tight_layout(pad=3.0)

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def update_from_slider(self):
        """Update labels when sliders move"""
        self.Xs_label.config(text=f"{self.Xs_pu.get():.2f}")
        self.V_label.config(text=f"{self.V_terminal_kV.get():.2f}")
        self.E_label.config(text=f"{self.E_initial_kV.get():.2f}")
        self.delta_label.config(text=f"{self.delta_initial_deg.get():.2f}")
        self.Pm_label.config(text=f"{self.Pm_pu.get():.2f}")
        self.H_label.config(text=f"{self.H.get():.2f}")
        self.D_label.config(text=f"{self.D.get():.3f}")
        self.sim_time_label.config(text=f"{self.sim_time.get():.1f}")

        # Auto-calculate
        self.calculate_all()

    def calculate_all(self):
        """Perform all calculations for parts (a) through (d)"""
        try:
            # Get values in per-unit (phase quantities)
            Xs = self.Xs_pu.get()
            # Convert line-line voltages to per-unit phase voltages
            # V_pu = (V_LL / sqrt(3)) / (V_base_LL / sqrt(3)) = V_LL / V_base_LL
            # Convert kV to V first, then divide by V_base_LL
            V_pu = (self.V_terminal_kV.get() * 1000) / self.V_base_LL
            E_pu = (self.E_initial_kV.get() * 1000) / self.V_base_LL
            delta_rad = np.radians(self.delta_initial_deg.get())

            # Part (a) - Initial condition
            E_complex = E_pu * np.exp(1j * delta_rad)
            V_complex = V_pu + 0j  # Reference at 0 degrees

            # Current: Ia = (E - V) / (jXs)
            Ia_complex = (E_complex - V_complex) / (1j * Xs)
            Ia_mag = np.abs(Ia_complex)
            Ia_angle = np.angle(Ia_complex)
            Ia_kA = Ia_mag * self.I_base / 1000  # Convert to kA

            # Part (b) - Power calculations
            # S = V * conj(Ia)
            S_complex = V_complex * np.conj(Ia_complex)
            P_pu = S_complex.real
            Q_pu = S_complex.imag
            P_MW = P_pu * self.S_base / 1e6
            Q_MVAR = Q_pu * self.S_base / 1e6

            # Power factor
            pf = np.cos(np.angle(V_complex) - Ia_angle)

            # Store results (a) and (b)
            self.results['a'] = {
                'Ia_pu': Ia_mag,
                'Ia_kA': Ia_kA,
                'Ia_angle_deg': np.degrees(Ia_angle),
                'I_base_kA': self.I_base / 1000
            }

            self.results['b'] = {
                'P_pu': P_pu,
                'Q_pu': Q_pu,
                'P_MW': P_MW,
                'Q_MVAR': Q_MVAR,
                'S_pu': np.abs(S_complex),
                'pf': pf
            }

            # Part (c) - Current reduced by 25%, same power factor
            Ia_new_mag = 0.75 * Ia_mag
            Ia_new_angle = Ia_angle  # Same power factor
            Ia_new_complex = Ia_new_mag * np.exp(1j * Ia_new_angle)

            # E = V + jXs * Ia
            E_new_c = V_complex + 1j * Xs * Ia_new_complex
            E_new_c_mag = np.abs(E_new_c)
            delta_new_c = np.angle(E_new_c)

            # Power for condition (c)
            S_new_c = V_complex * np.conj(Ia_new_complex)
            P_new_c = S_new_c.real
            Q_new_c = S_new_c.imag

            self.results['c'] = {
                'E_pu': E_new_c_mag,
                'E_kV_LL': E_new_c_mag * self.V_base_LL / 1000,  # Line-line kV
                'delta_rad': delta_new_c,
                'delta_deg': np.degrees(delta_new_c),
                'Ia_pu': Ia_new_mag,
                'Ia_kA': Ia_new_mag * self.I_base / 1000,
                'P_pu': P_new_c.real,
                'Q_pu': Q_new_c.imag,
                'pf': pf
            }

            # Part (d) - Unity power factor, same current magnitude as (c)
            # At pf = 1.0, Ia is in phase with V
            Ia_d_complex = Ia_new_mag + 0j  # Angle = 0 (in phase with V)

            # E = V + jXs * Ia
            E_new_d = V_complex + 1j * Xs * Ia_d_complex
            E_new_d_mag = np.abs(E_new_d)
            delta_new_d = np.angle(E_new_d)

            # Power for condition (d)
            S_new_d = V_complex * np.conj(Ia_d_complex)
            P_new_d = S_new_d.real
            Q_new_d = S_new_d.imag

            self.results['d'] = {
                'E_pu': E_new_d_mag,
                'E_kV_LL': E_new_d_mag * self.V_base_LL / 1000,  # Line-line kV
                'delta_rad': delta_new_d,
                'delta_deg': np.degrees(delta_new_d),
                'Ia_pu': Ia_new_mag,
                'Ia_kA': Ia_new_mag * self.I_base / 1000,
                'P_pu': P_new_d.real,
                'Q_pu': Q_new_d.imag,
                'pf': 1.0
            }

            # Store phasor data for plotting
            self.results['phasors'] = {
                'a': {'V': V_complex, 'E': E_complex, 'Ia': Ia_complex, 'Xs': Xs},
                'c': {'V': V_complex, 'E': E_new_c, 'Ia': Ia_new_complex, 'Xs': Xs},
                'd': {'V': V_complex, 'E': E_new_d, 'Ia': Ia_d_complex, 'Xs': Xs}
            }

            # Display results
            self.display_results()

            # Update plots
            self.update_plots()

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error in calculations: {str(e)}")

    def display_results(self):
        """Display calculation results in text widget"""
        self.results_text.delete(1.0, tk.END)

        text = "=" * 70 + "\n"
        text += "THREE-PHASE SYNCHRONOUS GENERATOR ANALYSIS\n"
        text += "=" * 70 + "\n\n"

        text += f"Base Values:\n"
        text += f"  S_base = {self.S_base/1e6:.1f} MVA\n"
        text += f"  V_base (L-L) = {self.V_base_LL/1e3:.1f} kV\n"
        text += f"  V_base (phase) = {self.V_base_phase/1e3:.3f} kV\n"
        text += f"  I_base = {self.I_base/1e3:.3f} kA\n"
        text += f"  Z_base = {self.Z_base:.3f} Ω\n\n"

        # Part (a)
        text += "-" * 70 + "\n"
        text += "Part (a): Per-phase line current\n"
        text += "-" * 70 + "\n"
        if 'a' in self.results:
            r = self.results['a']
            text += f"  |Ia| = {r['Ia_pu']:.4f} p.u. = {r['Ia_kA']:.4f} kA\n"
            text += f"  ∠Ia = {r['Ia_angle_deg']:.2f}°\n\n"

        # Part (b)
        text += "-" * 70 + "\n"
        text += "Part (b): Real and reactive power\n"
        text += "-" * 70 + "\n"
        if 'b' in self.results:
            r = self.results['b']
            text += f"  P = {r['P_pu']:.4f} p.u. = {r['P_MW']:.2f} MW\n"
            text += f"  Q = {r['Q_pu']:.4f} p.u. = {r['Q_MVAR']:.2f} MVAR\n"
            text += f"  S = {r['S_pu']:.4f} p.u.\n"
            text += f"  Power factor = {r['pf']:.4f} {'lagging' if r['Q_pu'] > 0 else 'leading'}\n\n"

        # Part (c)
        text += "-" * 70 + "\n"
        text += "Part (c): Current reduced by 25%, same power factor\n"
        text += "-" * 70 + "\n"
        if 'c' in self.results:
            r = self.results['c']
            text += f"  E = {r['E_pu']:.4f} p.u. = {r['E_kV_LL']:.3f} kV (line-line)\n"
            text += f"  δ = {r['delta_deg']:.2f}° = {r['delta_rad']:.4f} rad\n"
            text += f"  |Ia| = {r['Ia_pu']:.4f} p.u. = {r['Ia_kA']:.4f} kA\n"
            text += f"  P = {r['P_pu']:.4f} p.u. = {r['P_pu']*self.S_base/1e6:.2f} MW\n"
            text += f"  Q = {r['Q_pu']:.4f} p.u. = {r['Q_pu']*self.S_base/1e6:.2f} MVAR\n"
            text += f"  Power factor = {r['pf']:.4f}\n\n"

        # Part (d)
        text += "-" * 70 + "\n"
        text += "Part (d): Unity power factor, same current magnitude\n"
        text += "-" * 70 + "\n"
        if 'd' in self.results:
            r = self.results['d']
            text += f"  E = {r['E_pu']:.4f} p.u. = {r['E_kV_LL']:.3f} kV (line-line)\n"
            text += f"  δ = {r['delta_deg']:.2f}° = {r['delta_rad']:.4f} rad\n"
            text += f"  |Ia| = {r['Ia_pu']:.4f} p.u. = {r['Ia_kA']:.4f} kA\n"
            text += f"  P = {r['P_pu']:.4f} p.u. = {r['P_pu']*self.S_base/1e6:.2f} MW\n"
            text += f"  Q = {r['Q_pu']:.4f} p.u. = {r['Q_pu']*self.S_base/1e6:.2f} MVAR\n"
            text += f"  Power factor = {r['pf']:.4f}\n\n"

        text += "=" * 70 + "\n"

        self.results_text.insert(1.0, text)

    def update_plots(self):
        """Update all plots"""
        # Clear all axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Plot 1: Power-Angle Curve
        self.plot_power_angle_curve()

        # Plot 2: Phasor Diagrams
        self.plot_phasor_diagrams()

        # Plot 3 & 4: Will be updated by simulation
        if self.sim_data is not None:
            self.plot_simulation_results()
        else:
            self.ax3.text(0.5, 0.5, 'Run simulation to see results',
                         ha='center', va='center', transform=self.ax3.transAxes)
            self.ax4.text(0.5, 0.5, 'Run simulation to see results',
                         ha='center', va='center', transform=self.ax4.transAxes)
            self.ax3.set_xlabel('Time (s)')
            self.ax3.set_ylabel('δ (degrees)')
            self.ax3.set_title('Power Angle vs Time')
            self.ax3.grid(True)

            self.ax4.set_xlabel('Time (s)')
            self.ax4.set_ylabel('ω (rad/s)')
            self.ax4.set_title('Speed Deviation vs Time')
            self.ax4.grid(True)

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()

    def plot_power_angle_curve(self):
        """Plot electrical power vs power angle"""
        Xs = self.Xs_pu.get()
        V_pu = self.V_terminal_kV.get() / (self.V_base_LL / np.sqrt(3))
        E_pu = self.E_initial_kV.get() / (self.V_base_LL / np.sqrt(3))

        delta_range = np.linspace(0, 180, 1000)
        delta_rad_range = np.radians(delta_range)

        # Pe = (E * V / Xs) * sin(delta)
        Pe = (E_pu * V_pu / Xs) * np.sin(delta_rad_range)

        self.ax1.plot(delta_range, Pe, 'b-', linewidth=2, label='Pe(δ)')

        # Plot operating points
        if 'a' in self.results and 'b' in self.results:
            delta_a = self.delta_initial_deg.get()
            P_a = self.results['b']['P_pu']
            self.ax1.plot(delta_a, P_a, 'ro', markersize=10, label=f'Point (a): δ={delta_a:.1f}°')

        if 'c' in self.results:
            delta_c = self.results['c']['delta_deg']
            P_c = self.results['c']['P_pu']
            self.ax1.plot(delta_c, P_c, 'gs', markersize=10, label=f'Point (c): δ={delta_c:.1f}°')

        if 'd' in self.results:
            delta_d = self.results['d']['delta_deg']
            P_d = self.results['d']['P_pu']
            self.ax1.plot(delta_d, P_d, 'b^', markersize=10, label=f'Point (d): δ={delta_d:.1f}°')

        # Plot mechanical power line
        Pm = self.Pm_pu.get()
        self.ax1.axhline(y=Pm, color='r', linestyle='--', linewidth=1.5, label=f'Pm = {Pm:.2f} p.u.')

        self.ax1.set_xlabel('Power Angle δ (degrees)', fontsize=10)
        self.ax1.set_ylabel('Electrical Power Pe (p.u.)', fontsize=10)
        self.ax1.set_title('Power-Angle Characteristic', fontsize=11, fontweight='bold')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(fontsize=8, loc='upper right')
        self.ax1.set_xlim([0, 180])

    def plot_phasor_diagrams(self):
        """Plot phasor diagrams for all three conditions"""
        if 'phasors' not in self.results:
            return

        colors = {'a': 'red', 'c': 'green', 'd': 'blue'}
        labels = {'a': 'Condition (a)', 'c': 'Condition (c)', 'd': 'Condition (d)'}

        max_mag = 0

        for condition in ['a', 'c', 'd']:
            if condition not in self.results['phasors']:
                continue

            phasors = self.results['phasors'][condition]
            V = phasors['V']
            E = phasors['E']
            Ia = phasors['Ia']
            Xs = phasors['Xs']

            color = colors[condition]
            label = labels[condition]

            # Plot V (reference)
            if condition == 'a':
                self.ax2.arrow(0, 0, V.real, V.imag, head_width=0.05, head_length=0.05,
                              fc='black', ec='black', linewidth=2)
                self.ax2.text(V.real/2, V.imag/2 - 0.1, 'V', fontsize=10, fontweight='bold')

            # Plot E
            self.ax2.arrow(0, 0, E.real, E.imag, head_width=0.05, head_length=0.05,
                          fc=color, ec=color, linewidth=2, alpha=0.7, label=f'{label}: E')

            # Plot Ia (scaled for visibility)
            Ia_scaled = Ia * 0.5  # Scale current for better visualization
            self.ax2.arrow(0, 0, Ia_scaled.real, Ia_scaled.imag, head_width=0.05, head_length=0.05,
                          fc=color, ec=color, linewidth=1.5, linestyle='--', alpha=0.5)

            # Plot jXs*Ia
            jXsIa = 1j * Xs * Ia
            self.ax2.arrow(V.real, V.imag, jXsIa.real, jXsIa.imag,
                          head_width=0.05, head_length=0.05,
                          fc=color, ec=color, linewidth=1.5, linestyle=':', alpha=0.5)

            max_mag = max(max_mag, abs(E), abs(V), abs(jXsIa))

        self.ax2.set_xlabel('Real', fontsize=10)
        self.ax2.set_ylabel('Imaginary', fontsize=10)
        self.ax2.set_title('Phasor Diagrams (all conditions)', fontsize=11, fontweight='bold')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.axis('equal')
        self.ax2.legend(fontsize=8, loc='upper right')

        # Set limits
        margin = max_mag * 0.2
        self.ax2.set_xlim([-margin, max_mag + margin])
        self.ax2.set_ylim([-margin, max_mag + margin])

    def swing_equation(self, t, y, Pm, E, V, Xs, H, D):
        """
        Swing equation for synchronous generator
        y[0] = delta (power angle in radians)
        y[1] = omega (speed deviation in rad/s)
        """
        delta = y[0]
        omega = y[1]

        # Electrical power: Pe = (E*V/Xs) * sin(delta)
        Pe = (E * V / Xs) * np.sin(delta)

        # Swing equation: d(omega)/dt = (Pm - Pe - D*omega) / (2*H)
        # Note: omega_base = 2*pi*60 rad/s for 60 Hz system
        omega_base = 2 * np.pi * 60
        M = 2 * H / omega_base

        d_delta = omega
        d_omega = (Pm - Pe - D * omega) / M

        return [d_delta, d_omega]

    def euler_method(self, f, t_span, y0, t_eval, args):
        """Custom Euler method implementation"""
        t0, tf = t_span
        dt = t_eval[1] - t_eval[0] if len(t_eval) > 1 else 0.01

        t_values = [t0]
        y_values = [y0]

        t = t0
        y = np.array(y0)

        for t_next in t_eval[1:]:
            while t < t_next:
                step = min(dt, t_next - t)
                dydt = np.array(f(t, y, *args))
                y = y + step * dydt
                t = t + step

            t_values.append(t)
            y_values.append(y.copy())

        return t_values, np.array(y_values).T

    def run_simulation(self):
        """Run dynamic simulation using ODE solver"""
        try:
            # Get parameters
            Xs = self.Xs_pu.get()
            V_pu = self.V_terminal_kV.get() / (self.V_base_LL / np.sqrt(3))
            E_pu = self.E_initial_kV.get() / (self.V_base_LL / np.sqrt(3))
            delta0_rad = np.radians(self.delta_initial_deg.get())
            Pm = self.Pm_pu.get()
            H = self.H.get()
            D = self.D.get()

            # Initial conditions: [delta, omega]
            y0 = [delta0_rad, 0.0]

            # Time span
            t_span = (0, self.sim_time.get())
            t_eval = np.linspace(0, self.sim_time.get(), int(self.sim_time.get() / self.time_step.get()))

            # Solve using selected method
            if self.solver_type.get() == "RK45":
                sol = solve_ivp(
                    self.swing_equation,
                    t_span,
                    y0,
                    args=(Pm, E_pu, V_pu, Xs, H, D),
                    method='RK45',
                    t_eval=t_eval,
                    dense_output=True
                )
                t_result = sol.t
                delta_result = sol.y[0]
                omega_result = sol.y[1]
            else:  # Euler
                t_result, y_result = self.euler_method(
                    self.swing_equation,
                    t_span,
                    y0,
                    t_eval,
                    args=(Pm, E_pu, V_pu, Xs, H, D)
                )
                delta_result = y_result[0]
                omega_result = y_result[1]

            # Store simulation data
            self.sim_data = {
                't': t_result,
                'delta': delta_result,
                'omega': omega_result
            }

            # Update plots
            self.plot_simulation_results()
            self.canvas.draw()

            messagebox.showinfo("Simulation Complete",
                               f"Simulation completed using {self.solver_type.get()} method.\n"
                               f"Time: 0 to {self.sim_time.get():.1f} seconds")

        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error in simulation: {str(e)}")

    def plot_simulation_results(self):
        """Plot simulation results"""
        if self.sim_data is None:
            return

        t = self.sim_data['t']
        delta = np.degrees(self.sim_data['delta'])  # Convert to degrees
        omega = self.sim_data['omega']

        # Plot delta vs time
        self.ax3.clear()
        self.ax3.plot(t, delta, 'b-', linewidth=2)
        self.ax3.set_xlabel('Time (s)', fontsize=10)
        self.ax3.set_ylabel('Power Angle δ (degrees)', fontsize=10)
        self.ax3.set_title(f'Power Angle vs Time ({self.solver_type.get()} solver)',
                          fontsize=11, fontweight='bold')
        self.ax3.grid(True, alpha=0.3)

        # Add animation marker if running
        if self.is_running and hasattr(self, 'current_time_index'):
            idx = self.current_time_index
            if idx < len(t):
                self.ax3.plot(t[idx], delta[idx], 'ro', markersize=8)

        # Plot omega vs time
        self.ax4.clear()
        self.ax4.plot(t, omega, 'r-', linewidth=2)
        self.ax4.set_xlabel('Time (s)', fontsize=10)
        self.ax4.set_ylabel('Speed Deviation ω (rad/s)', fontsize=10)
        self.ax4.set_title(f'Speed Deviation vs Time ({self.solver_type.get()} solver)',
                          fontsize=11, fontweight='bold')
        self.ax4.grid(True, alpha=0.3)

        # Add animation marker if running
        if self.is_running and hasattr(self, 'current_time_index'):
            idx = self.current_time_index
            if idx < len(t):
                self.ax4.plot(t[idx], omega[idx], 'ro', markersize=8)

    def toggle_animation(self):
        """Toggle animation on/off"""
        if self.sim_data is None:
            messagebox.showwarning("No Simulation", "Please run simulation first!")
            return

        if self.is_running:
            self.stop_animation()
        else:
            self.start_animation()

    def start_animation(self):
        """Start animation of simulation results"""
        self.is_running = True
        self.current_time_index = 0
        self.anim_button.config(text="Stop Animation")
        self.animate()

    def stop_animation(self):
        """Stop animation"""
        self.is_running = False
        self.anim_button.config(text="Start Animation")
        if self.animation_id:
            self.root.after_cancel(self.animation_id)

    def animate(self):
        """Animation step"""
        if not self.is_running:
            return

        if self.current_time_index >= len(self.sim_data['t']):
            self.current_time_index = 0  # Loop animation

        # Update plots with current time marker
        self.plot_simulation_results()
        self.canvas.draw()

        self.current_time_index += 1

        # Schedule next frame (30 fps)
        self.animation_id = self.root.after(33, self.animate)

    def reset_parameters(self):
        """Reset all parameters to default values"""
        self.Xs_pu.set(1.60)
        self.V_terminal_kV.set(15.0)
        self.E_initial_kV.set(24.0)
        self.delta_initial_deg.set(25.0)
        self.Pm_pu.set(0.8)
        self.H.set(3.5)
        self.D.set(0.05)
        self.sim_time.set(5.0)
        self.time_step.set(0.01)
        self.solver_type.set("RK45")

        self.update_from_slider()
        self.calculate_all()

    def on_resize(self, event):
        """Handle window resize event"""
        # Only respond to main window resize, not child widgets
        if event.widget == self.root:
            try:
                self.fig.tight_layout(pad=2.0)
                self.canvas.draw_idle()
            except Exception:
                pass  # Ignore resize errors during initialization


def main():
    root = tk.Tk()
    app = SynchronousGeneratorSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
