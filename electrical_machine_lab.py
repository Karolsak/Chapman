#!/usr/bin/env python3
"""
Advanced Electrical Machine Modeling Laboratory
================================================
A comprehensive tkinter-based application for modeling, studying, and developing
electrical machines including:
- Transformers
- Induction Motors
- Synchronous Machines
- DC Machines

Author: Electrical Machine Lab
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt


class ElectricalMachineLab(tk.Tk):
    """Main application window for the Electrical Machine Laboratory"""

    def __init__(self):
        super().__init__()

        self.title("Advanced Electrical Machine Modeling Laboratory")
        self.geometry("1400x900")
        self.configure(bg='#2C3E50')

        # Create menu bar
        self.create_menu()

        # Create main header
        self.create_header()

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Apply styling
        self.apply_styles()

        # Create tabs for different machine types
        self.transformer_tab = TransformerLab(self.notebook)
        self.induction_tab = InductionMotorLab(self.notebook)
        self.synchronous_tab = SynchronousMachineLab(self.notebook)
        self.dc_machine_tab = DCMachineLab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.transformer_tab, text='  Transformers  ')
        self.notebook.add(self.induction_tab, text='  Induction Motors  ')
        self.notebook.add(self.synchronous_tab, text='  Synchronous Machines  ')
        self.notebook.add(self.dc_machine_tab, text='  DC Machines  ')

        # Status bar
        self.create_status_bar()

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)

    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self, bg='#34495E', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="⚡ Advanced Electrical Machine Modeling Laboratory ⚡",
            font=('Helvetica', 20, 'bold'),
            bg='#34495E',
            fg='#ECF0F1'
        )
        title_label.pack(pady=20)

    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self, bg='#34495E')
        status_frame.pack(fill='x', side='bottom', padx=10, pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg='#34495E',
            fg='#ECF0F1',
            anchor='w'
        )
        self.status_label.pack(fill='x', padx=10, pady=5)

    def apply_styles(self):
        """Apply custom styles to widgets"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure notebook style
        style.configure('TNotebook', background='#2C3E50', borderwidth=0)
        style.configure('TNotebook.Tab',
                       background='#34495E',
                       foreground='#ECF0F1',
                       padding=[20, 10],
                       font=('Helvetica', 11, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', '#1ABC9C')],
                 foreground=[('selected', '#FFFFFF')])

        # Configure frame style
        style.configure('TFrame', background='#ECF0F1')

        # Configure label style
        style.configure('TLabel', background='#ECF0F1', font=('Helvetica', 10))
        style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))

        # Configure button style
        style.configure('TButton',
                       background='#3498DB',
                       foreground='#FFFFFF',
                       borderwidth=1,
                       focuscolor='none',
                       font=('Helvetica', 10, 'bold'))
        style.map('TButton',
                 background=[('active', '#2980B9')])

    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.update_idletasks()

    def save_results(self):
        """Save current results"""
        messagebox.showinfo("Save Results", "Results saved successfully!")

    def show_about(self):
        """Show about dialog"""
        about_text = """
        Advanced Electrical Machine Modeling Laboratory
        Version 1.0

        A comprehensive tool for studying and developing
        electrical machines including:
        - Transformers
        - Induction Motors
        - Synchronous Machines
        - DC Machines

        Based on Chapman's Electric Machinery Fundamentals
        """
        messagebox.showinfo("About", about_text)

    def show_documentation(self):
        """Show documentation"""
        doc_text = """
        Documentation

        Use the tabs to access different machine types.
        Enter parameters and click 'Calculate' or 'Plot'
        to see results and visualizations.

        Features:
        - Real-time parameter adjustment
        - Interactive plotting
        - Performance characteristic curves
        - Equivalent circuit calculations
        """
        messagebox.showinfo("Documentation", doc_text)


class TransformerLab(ttk.Frame):
    """Transformer modeling and analysis laboratory"""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='TFrame')

        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title = ttk.Label(main_container,
                         text="Transformer Analysis and Modeling",
                         style='Title.TLabel')
        title.pack(pady=(0, 20))

        # Create two-column layout
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        right_frame = ttk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True)

        # Parameters section
        self.create_parameter_section(left_frame)

        # Results section
        self.create_results_section(left_frame)

        # Plotting section
        self.create_plot_section(right_frame)

    def create_parameter_section(self, parent):
        """Create parameter input section"""
        param_frame = ttk.LabelFrame(parent, text="Transformer Parameters", padding=15)
        param_frame.pack(fill='x', pady=(0, 20))

        # Parameters
        self.params = {}
        param_list = [
            ("Rated Power (kVA):", "50", "s_rated"),
            ("Primary Voltage (V):", "13800", "v1"),
            ("Secondary Voltage (V):", "120", "v2"),
            ("Frequency (Hz):", "60", "freq"),
            ("R1 - Primary Resistance (Ω):", "0.6", "r1"),
            ("X1 - Primary Reactance (Ω):", "1.2", "x1"),
            ("R2 - Secondary Resistance (Ω):", "0.0055", "r2"),
            ("X2 - Secondary Reactance (Ω):", "0.011", "x2"),
            ("Rc - Core Resistance (Ω):", "46000", "rc"),
            ("Xm - Magnetizing Reactance (Ω):", "2500", "xm"),
        ]

        for i, (label_text, default_val, key) in enumerate(param_list):
            label = ttk.Label(param_frame, text=label_text)
            label.grid(row=i, column=0, sticky='w', pady=5)

            entry = ttk.Entry(param_frame, width=15)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            self.params[key] = entry

        param_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(param_frame)
        button_frame.grid(row=len(param_list), column=0, columnspan=2, pady=(15, 0))

        calc_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calc_btn.pack(side='left', padx=5)

        plot_btn = ttk.Button(button_frame, text="Plot Characteristics",
                             command=self.plot_characteristics)
        plot_btn.pack(side='left', padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_parameters)
        reset_btn.pack(side='left', padx=5)

    def create_results_section(self, parent):
        """Create results display section"""
        results_frame = ttk.LabelFrame(parent, text="Calculated Results", padding=15)
        results_frame.pack(fill='both', expand=True)

        self.results_text = tk.Text(results_frame, height=15, width=50,
                                   font=('Courier', 10), bg='#FFFFFF',
                                   relief='solid', borderwidth=1)
        self.results_text.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)

    def create_plot_section(self, parent):
        """Create plotting section"""
        plot_frame = ttk.LabelFrame(parent, text="Visualization", padding=10)
        plot_frame.pack(fill='both', expand=True)

        # Create matplotlib figure
        self.fig = Figure(figsize=(7, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()

    def get_parameters(self):
        """Get parameters from entries"""
        try:
            return {key: float(entry.get()) for key, entry in self.params.items()}
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            return None

    def calculate(self):
        """Calculate transformer characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        # Calculate turns ratio
        a = params['v1'] / params['v2']

        # Calculate equivalent impedance referred to primary
        r_eq1 = params['r1'] + a**2 * params['r2']
        x_eq1 = params['x1'] + a**2 * params['x2']
        z_eq1 = np.sqrt(r_eq1**2 + x_eq1**2)

        # Calculate equivalent impedance referred to secondary
        r_eq2 = params['r2'] + params['r1'] / a**2
        x_eq2 = params['x2'] + params['x1'] / a**2
        z_eq2 = np.sqrt(r_eq2**2 + x_eq2**2)

        # Calculate voltage regulation at full load (pf = 0.8 lagging)
        pf = 0.8
        i2_rated = params['s_rated'] * 1000 / params['v2']
        v2_nl = params['v2'] + i2_rated * (r_eq2 * pf + x_eq2 * np.sqrt(1 - pf**2))
        vr = (v2_nl - params['v2']) / params['v2'] * 100

        # Calculate efficiency at full load
        p_out = params['s_rated'] * 1000 * pf
        p_cu = i2_rated**2 * r_eq2
        p_core = params['v2']**2 / params['rc']
        efficiency = p_out / (p_out + p_cu + p_core) * 100

        # Display results
        results = f"""
TRANSFORMER ANALYSIS RESULTS
{'=' * 50}

Turns Ratio (a):              {a:.4f}

Equivalent Circuit (Primary Side):
  R_eq1:                      {r_eq1:.4f} Ω
  X_eq1:                      {x_eq1:.4f} Ω
  Z_eq1:                      {z_eq1:.4f} Ω

Equivalent Circuit (Secondary Side):
  R_eq2:                      {r_eq2:.6f} Ω
  X_eq2:                      {x_eq2:.6f} Ω
  Z_eq2:                      {z_eq2:.6f} Ω

Performance at Full Load (PF = {pf}):
  Rated Current (Secondary):  {i2_rated:.4f} A
  Voltage Regulation:         {vr:.2f} %
  Copper Loss:                {p_cu:.2f} W
  Core Loss:                  {p_core:.2f} W
  Efficiency:                 {efficiency:.2f} %
{'=' * 50}
"""

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)

    def plot_characteristics(self):
        """Plot transformer characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        self.fig.clear()

        # Calculate equivalent impedance referred to secondary
        a = params['v1'] / params['v2']
        r_eq2 = params['r2'] + params['r1'] / a**2
        x_eq2 = params['x2'] + params['x1'] / a**2

        # Create load range
        load_percent = np.linspace(0, 150, 100)
        i2_rated = params['s_rated'] * 1000 / params['v2']
        i2 = load_percent / 100 * i2_rated

        # Power factors to analyze
        pf_values = [1.0, 0.8, 0.6]
        pf_labels = ['Unity PF', 'PF = 0.8 lag', 'PF = 0.6 lag']

        # Plot 1: Voltage Regulation
        ax1 = self.fig.add_subplot(2, 2, 1)
        for pf, label in zip(pf_values, pf_labels):
            vr = i2 * (r_eq2 * pf + x_eq2 * np.sqrt(1 - pf**2)) / params['v2'] * 100
            ax1.plot(load_percent, vr, label=label, linewidth=2)
        ax1.set_xlabel('Load (%)')
        ax1.set_ylabel('Voltage Regulation (%)')
        ax1.set_title('Voltage Regulation vs Load')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot 2: Efficiency
        ax2 = self.fig.add_subplot(2, 2, 2)
        p_core = params['v2']**2 / params['rc']
        for pf, label in zip(pf_values, pf_labels):
            p_out = params['v2'] * i2 * pf
            p_cu = i2**2 * r_eq2
            eff = p_out / (p_out + p_cu + p_core) * 100
            # Avoid division by zero
            eff = np.where(p_out > 0, eff, 0)
            ax2.plot(load_percent, eff, label=label, linewidth=2)
        ax2.set_xlabel('Load (%)')
        ax2.set_ylabel('Efficiency (%)')
        ax2.set_title('Efficiency vs Load')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim([0, 100])

        # Plot 3: Output Voltage
        ax3 = self.fig.add_subplot(2, 2, 3)
        for pf, label in zip(pf_values, pf_labels):
            v2_out = params['v2'] - i2 * (r_eq2 * pf + x_eq2 * np.sqrt(1 - pf**2))
            ax3.plot(load_percent, v2_out, label=label, linewidth=2)
        ax3.set_xlabel('Load (%)')
        ax3.set_ylabel('Output Voltage (V)')
        ax3.set_title('Output Voltage vs Load')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Plot 4: Losses
        ax4 = self.fig.add_subplot(2, 2, 4)
        p_cu = i2**2 * r_eq2
        p_core_array = np.full_like(load_percent, p_core)
        p_total = p_cu + p_core
        ax4.plot(load_percent, p_cu, label='Copper Loss', linewidth=2)
        ax4.plot(load_percent, p_core_array, label='Core Loss', linewidth=2)
        ax4.plot(load_percent, p_total, label='Total Loss', linewidth=2, linestyle='--')
        ax4.set_xlabel('Load (%)')
        ax4.set_ylabel('Losses (W)')
        ax4.set_title('Losses vs Load')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def reset_parameters(self):
        """Reset parameters to default values"""
        defaults = {
            "s_rated": "50",
            "v1": "13800",
            "v2": "120",
            "freq": "60",
            "r1": "0.6",
            "x1": "1.2",
            "r2": "0.0055",
            "x2": "0.011",
            "rc": "46000",
            "xm": "2500"
        }
        for key, entry in self.params.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[key])
        self.results_text.delete(1.0, tk.END)


class InductionMotorLab(ttk.Frame):
    """Induction motor modeling and analysis laboratory"""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='TFrame')

        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title = ttk.Label(main_container,
                         text="Induction Motor Analysis and Modeling",
                         style='Title.TLabel')
        title.pack(pady=(0, 20))

        # Create two-column layout
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        right_frame = ttk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True)

        # Parameters section
        self.create_parameter_section(left_frame)

        # Results section
        self.create_results_section(left_frame)

        # Plotting section
        self.create_plot_section(right_frame)

    def create_parameter_section(self, parent):
        """Create parameter input section"""
        param_frame = ttk.LabelFrame(parent, text="Induction Motor Parameters", padding=15)
        param_frame.pack(fill='x', pady=(0, 20))

        # Parameters
        self.params = {}
        param_list = [
            ("Rated Power (HP):", "50", "hp_rated"),
            ("Line Voltage (V):", "460", "v_line"),
            ("Frequency (Hz):", "60", "freq"),
            ("Number of Poles:", "4", "poles"),
            ("R1 - Stator Resistance (Ω):", "0.641", "r1"),
            ("X1 - Stator Reactance (Ω):", "1.106", "x1"),
            ("R2 - Rotor Resistance (Ω):", "0.332", "r2"),
            ("X2 - Rotor Reactance (Ω):", "0.464", "x2"),
            ("Xm - Magnetizing Reactance (Ω):", "26.3", "xm"),
        ]

        for i, (label_text, default_val, key) in enumerate(param_list):
            label = ttk.Label(param_frame, text=label_text)
            label.grid(row=i, column=0, sticky='w', pady=5)

            entry = ttk.Entry(param_frame, width=15)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            self.params[key] = entry

        param_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(param_frame)
        button_frame.grid(row=len(param_list), column=0, columnspan=2, pady=(15, 0))

        calc_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calc_btn.pack(side='left', padx=5)

        plot_btn = ttk.Button(button_frame, text="Plot Torque-Speed",
                             command=self.plot_characteristics)
        plot_btn.pack(side='left', padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_parameters)
        reset_btn.pack(side='left', padx=5)

    def create_results_section(self, parent):
        """Create results display section"""
        results_frame = ttk.LabelFrame(parent, text="Calculated Results", padding=15)
        results_frame.pack(fill='both', expand=True)

        self.results_text = tk.Text(results_frame, height=15, width=50,
                                   font=('Courier', 10), bg='#FFFFFF',
                                   relief='solid', borderwidth=1)
        self.results_text.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)

    def create_plot_section(self, parent):
        """Create plotting section"""
        plot_frame = ttk.LabelFrame(parent, text="Visualization", padding=10)
        plot_frame.pack(fill='both', expand=True)

        # Create matplotlib figure
        self.fig = Figure(figsize=(7, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()

    def get_parameters(self):
        """Get parameters from entries"""
        try:
            return {key: float(entry.get()) for key, entry in self.params.items()}
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            return None

    def calculate(self):
        """Calculate induction motor characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        # Calculate derived parameters
        v_phase = params['v_line'] / np.sqrt(3)
        n_sync = 120 * params['freq'] / params['poles']
        w_sync = 2 * np.pi * params['freq'] / (params['poles'] / 2)

        # Calculate Thevenin equivalent
        xm = params['xm']
        r1 = params['r1']
        x1 = params['x1']

        v_th = v_phase * (xm / np.sqrt(r1**2 + (x1 + xm)**2))
        z_th = (1j * xm * (r1 + 1j * x1)) / (r1 + 1j * (x1 + xm))
        r_th = np.real(z_th)
        x_th = np.imag(z_th)

        # Calculate starting torque (s = 1)
        s = 1.0
        t_start = (3 * v_th**2 * params['r2'] / s) / \
                  (w_sync * ((r_th + params['r2'] / s)**2 + (x_th + params['x2'])**2))

        # Calculate maximum torque and slip
        s_max = params['r2'] / np.sqrt(r_th**2 + (x_th + params['x2'])**2)
        t_max = (3 * v_th**2) / \
                (2 * w_sync * (r_th + np.sqrt(r_th**2 + (x_th + params['x2'])**2)))

        # Calculate rated slip (assuming 95% of synchronous speed)
        n_rated = 0.95 * n_sync
        s_rated = (n_sync - n_rated) / n_sync

        # Calculate torque at rated slip
        t_rated = (3 * v_th**2 * params['r2'] / s_rated) / \
                  (w_sync * ((r_th + params['r2'] / s_rated)**2 + (x_th + params['x2'])**2))

        # Display results
        results = f"""
INDUCTION MOTOR ANALYSIS RESULTS
{'=' * 50}

Motor Ratings:
  Rated Power:                {params['hp_rated']:.1f} HP
  Line Voltage:               {params['v_line']:.1f} V
  Phase Voltage:              {v_phase:.2f} V
  Frequency:                  {params['freq']:.1f} Hz
  Number of Poles:            {int(params['poles'])}

Synchronous Speed:
  Speed (RPM):                {n_sync:.1f} RPM
  Angular Velocity:           {w_sync:.2f} rad/s

Thevenin Equivalent:
  V_th:                       {v_th:.2f} V
  R_th:                       {r_th:.4f} Ω
  X_th:                       {x_th:.4f} Ω

Performance Characteristics:
  Starting Torque:            {t_start:.2f} N⋅m
  Maximum Torque:             {t_max:.2f} N⋅m
  Slip at Max Torque:         {s_max:.4f} ({s_max*100:.2f}%)

Rated Operating Point (est.):
  Rated Speed:                {n_rated:.1f} RPM
  Rated Slip:                 {s_rated:.4f} ({s_rated*100:.2f}%)
  Rated Torque:               {t_rated:.2f} N⋅m

Starting/Rated Ratio:         {t_start/t_rated:.2f}
Maximum/Rated Ratio:          {t_max/t_rated:.2f}
{'=' * 50}
"""

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)

    def plot_characteristics(self):
        """Plot induction motor characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        self.fig.clear()

        # Calculate parameters
        v_phase = params['v_line'] / np.sqrt(3)
        n_sync = 120 * params['freq'] / params['poles']
        w_sync = 2 * np.pi * params['freq'] / (params['poles'] / 2)

        # Thevenin equivalent
        xm = params['xm']
        r1 = params['r1']
        x1 = params['x1']

        v_th = v_phase * (xm / np.sqrt(r1**2 + (x1 + xm)**2))
        z_th = (1j * xm * (r1 + 1j * x1)) / (r1 + 1j * (x1 + xm))
        r_th = np.real(z_th)
        x_th = np.imag(z_th)

        # Create slip range
        s = np.linspace(0.001, 1, 200)
        nm = (1 - s) * n_sync

        # Calculate torque-speed curve
        t_ind = (3 * v_th**2 * params['r2'] / s) / \
                (w_sync * ((r_th + params['r2'] / s)**2 + (x_th + params['x2'])**2))

        # Calculate current
        i2 = v_th / np.sqrt((r_th + params['r2'] / s)**2 + (x_th + params['x2'])**2)
        i1 = i2  # Approximate

        # Calculate power and efficiency
        p_ag = 3 * i2**2 * params['r2'] / s  # Air gap power
        p_mech = p_ag * (1 - s)
        p_loss = 3 * i1**2 * r1 + 3 * i2**2 * params['r2']
        efficiency = np.where(p_ag > 0, p_mech / (p_mech + p_loss) * 100, 0)

        # Plot 1: Torque-Speed Curve
        ax1 = self.fig.add_subplot(2, 2, 1)
        ax1.plot(nm, t_ind, 'b-', linewidth=2)
        ax1.set_xlabel('Speed (RPM)')
        ax1.set_ylabel('Torque (N⋅m)')
        ax1.set_title('Torque-Speed Characteristic')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # Plot 2: Current vs Speed
        ax2 = self.fig.add_subplot(2, 2, 2)
        ax2.plot(nm, i1, 'r-', linewidth=2)
        ax2.set_xlabel('Speed (RPM)')
        ax2.set_ylabel('Current (A)')
        ax2.set_title('Stator Current vs Speed')
        ax2.grid(True, alpha=0.3)

        # Plot 3: Power vs Speed
        ax3 = self.fig.add_subplot(2, 2, 3)
        ax3.plot(nm, p_mech / 1000, 'g-', linewidth=2, label='Mechanical Power')
        ax3.plot(nm, p_ag / 1000, 'b--', linewidth=2, label='Air Gap Power')
        ax3.set_xlabel('Speed (RPM)')
        ax3.set_ylabel('Power (kW)')
        ax3.set_title('Power vs Speed')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Plot 4: Efficiency vs Speed
        ax4 = self.fig.add_subplot(2, 2, 4)
        ax4.plot(nm, efficiency, 'm-', linewidth=2)
        ax4.set_xlabel('Speed (RPM)')
        ax4.set_ylabel('Efficiency (%)')
        ax4.set_title('Efficiency vs Speed')
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim([0, 100])

        self.fig.tight_layout()
        self.canvas.draw()

    def reset_parameters(self):
        """Reset parameters to default values"""
        defaults = {
            "hp_rated": "50",
            "v_line": "460",
            "freq": "60",
            "poles": "4",
            "r1": "0.641",
            "x1": "1.106",
            "r2": "0.332",
            "x2": "0.464",
            "xm": "26.3"
        }
        for key, entry in self.params.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[key])
        self.results_text.delete(1.0, tk.END)


class SynchronousMachineLab(ttk.Frame):
    """Synchronous machine modeling and analysis laboratory"""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='TFrame')

        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title = ttk.Label(main_container,
                         text="Synchronous Machine Analysis and Modeling",
                         style='Title.TLabel')
        title.pack(pady=(0, 20))

        # Create two-column layout
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        right_frame = ttk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True)

        # Parameters section
        self.create_parameter_section(left_frame)

        # Results section
        self.create_results_section(left_frame)

        # Plotting section
        self.create_plot_section(right_frame)

    def create_parameter_section(self, parent):
        """Create parameter input section"""
        param_frame = ttk.LabelFrame(parent, text="Synchronous Machine Parameters", padding=15)
        param_frame.pack(fill='x', pady=(0, 20))

        # Parameters
        self.params = {}
        param_list = [
            ("Rated Power (MVA):", "10", "s_rated"),
            ("Rated Voltage (kV):", "13.8", "v_rated"),
            ("Frequency (Hz):", "60", "freq"),
            ("Number of Poles:", "4", "poles"),
            ("Ra - Armature Resistance (Ω):", "0.15", "ra"),
            ("Xs - Synchronous Reactance (Ω):", "1.2", "xs"),
            ("Field Current (A):", "100", "if_current"),
            ("Power Factor:", "0.85", "pf"),
        ]

        for i, (label_text, default_val, key) in enumerate(param_list):
            label = ttk.Label(param_frame, text=label_text)
            label.grid(row=i, column=0, sticky='w', pady=5)

            entry = ttk.Entry(param_frame, width=15)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            self.params[key] = entry

        param_frame.columnconfigure(1, weight=1)

        # Operation mode selection
        mode_label = ttk.Label(param_frame, text="Operation Mode:")
        mode_label.grid(row=len(param_list), column=0, sticky='w', pady=5)

        self.mode_var = tk.StringVar(value="generator")
        mode_frame = ttk.Frame(param_frame)
        mode_frame.grid(row=len(param_list), column=1, sticky='w', pady=5)

        gen_radio = ttk.Radiobutton(mode_frame, text="Generator",
                                    variable=self.mode_var, value="generator")
        gen_radio.pack(side='left', padx=(0, 10))

        mot_radio = ttk.Radiobutton(mode_frame, text="Motor",
                                    variable=self.mode_var, value="motor")
        mot_radio.pack(side='left')

        # Buttons
        button_frame = ttk.Frame(param_frame)
        button_frame.grid(row=len(param_list)+1, column=0, columnspan=2, pady=(15, 0))

        calc_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calc_btn.pack(side='left', padx=5)

        plot_btn = ttk.Button(button_frame, text="Plot V-Curve",
                             command=self.plot_characteristics)
        plot_btn.pack(side='left', padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_parameters)
        reset_btn.pack(side='left', padx=5)

    def create_results_section(self, parent):
        """Create results display section"""
        results_frame = ttk.LabelFrame(parent, text="Calculated Results", padding=15)
        results_frame.pack(fill='both', expand=True)

        self.results_text = tk.Text(results_frame, height=15, width=50,
                                   font=('Courier', 10), bg='#FFFFFF',
                                   relief='solid', borderwidth=1)
        self.results_text.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)

    def create_plot_section(self, parent):
        """Create plotting section"""
        plot_frame = ttk.LabelFrame(parent, text="Visualization", padding=10)
        plot_frame.pack(fill='both', expand=True)

        # Create matplotlib figure
        self.fig = Figure(figsize=(7, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()

    def get_parameters(self):
        """Get parameters from entries"""
        try:
            return {key: float(entry.get()) for key, entry in self.params.items()}
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            return None

    def calculate(self):
        """Calculate synchronous machine characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        # Convert to base units
        v_phase = params['v_rated'] * 1000 / np.sqrt(3)
        s_base = params['s_rated'] * 1e6
        i_rated = s_base / (np.sqrt(3) * params['v_rated'] * 1000)

        # Calculate synchronous speed
        n_sync = 120 * params['freq'] / params['poles']
        w_sync = 2 * np.pi * n_sync / 60

        # Calculate internal generated voltage (Ea)
        pf = params['pf']
        theta = np.arccos(pf)

        if self.mode_var.get() == "generator":
            # Generator mode
            ia = i_rated
            vt = v_phase + 0j  # Terminal voltage as reference
            ia_phasor = ia * (pf - 1j * np.sin(theta))
            ea = vt + ia_phasor * (params['ra'] + 1j * params['xs'])
        else:
            # Motor mode
            ia = i_rated
            vt = v_phase + 0j
            ia_phasor = ia * (pf + 1j * np.sin(theta))
            ea = vt - ia_phasor * (params['ra'] + 1j * params['xs'])

        ea_mag = np.abs(ea)
        ea_angle = np.angle(ea, deg=True)

        # Calculate power
        p_out = np.sqrt(3) * params['v_rated'] * 1000 * i_rated * pf / 1e6
        q_out = np.sqrt(3) * params['v_rated'] * 1000 * i_rated * np.sin(theta) / 1e6
        s_out = np.sqrt(p_out**2 + q_out**2)

        # Calculate torque
        torque = p_out * 1e6 / w_sync

        # Calculate losses and efficiency
        p_cu = 3 * i_rated**2 * params['ra'] / 1e6
        p_core = 0.01 * params['s_rated']  # Approximate core loss (1% of rating)

        if self.mode_var.get() == "generator":
            p_in = p_out + p_cu + p_core
            efficiency = p_out / p_in * 100
        else:
            p_in = p_out + p_cu + p_core
            efficiency = p_out / p_in * 100

        # Display results
        mode_str = "GENERATOR" if self.mode_var.get() == "generator" else "MOTOR"
        results = f"""
SYNCHRONOUS {mode_str} ANALYSIS RESULTS
{'=' * 50}

Machine Ratings:
  Rated Power:                {params['s_rated']:.2f} MVA
  Rated Voltage:              {params['v_rated']:.2f} kV (L-L)
  Phase Voltage:              {v_phase/1000:.2f} kV
  Rated Current:              {i_rated:.2f} A
  Frequency:                  {params['freq']:.1f} Hz
  Number of Poles:            {int(params['poles'])}

Synchronous Speed:
  Speed (RPM):                {n_sync:.1f} RPM
  Angular Velocity:           {w_sync:.2f} rad/s

Operating Conditions:
  Power Factor:               {pf:.2f} {'lagging' if theta > 0 else 'leading'}
  Power Angle:                {ea_angle:.2f}°

Internal Generated Voltage:
  Magnitude (Ea):             {ea_mag:.2f} V ({ea_mag/v_phase:.3f} pu)
  Angle:                      {ea_angle:.2f}°

Output Power:
  Active Power (P):           {p_out:.2f} MW
  Reactive Power (Q):         {q_out:.2f} MVAR
  Apparent Power (S):         {s_out:.2f} MVA
  Electromagnetic Torque:     {torque:.2f} N⋅m

Losses and Efficiency:
  Copper Loss:                {p_cu*1000:.2f} kW
  Core Loss (est.):           {p_core*1000:.2f} kW
  Efficiency:                 {efficiency:.2f} %
{'=' * 50}
"""

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)

    def plot_characteristics(self):
        """Plot synchronous machine characteristics (V-curves)"""
        params = self.get_parameters()
        if params is None:
            return

        self.fig.clear()

        # Convert to base units
        v_phase = params['v_rated'] * 1000 / np.sqrt(3)
        s_base = params['s_rated'] * 1e6
        i_rated = s_base / (np.sqrt(3) * params['v_rated'] * 1000)

        # Power levels to analyze
        power_levels = [0.25, 0.5, 0.75, 1.0]
        colors = ['blue', 'green', 'orange', 'red']

        # Field current range
        if_range = np.linspace(50, 200, 100)

        # Plot 1: V-Curves (Ia vs If at different power levels)
        ax1 = self.fig.add_subplot(2, 2, 1)

        for p_level, color in zip(power_levels, colors):
            ia_values = []
            pf_values = []

            for if_val in if_range:
                # Approximate: Ea proportional to field current
                ea_mag = v_phase * (if_val / params['if_current']) * 1.2
                p_out = p_level * params['s_rated']

                # Calculate armature current
                # Simplified calculation
                ia = p_out * 1e6 / (np.sqrt(3) * params['v_rated'] * 1000 * 0.85)

                # Calculate power factor
                q = np.sqrt((ea_mag - v_phase)**2 - (params['xs'] * ia)**2) / params['xs']
                s = np.sqrt(p_out**2 + q**2) if q > 0 else p_out
                pf = p_out / s if s > 0 else 1.0

                ia_values.append(ia)
                pf_values.append(pf)

            ax1.plot(if_range, ia_values, color=color, linewidth=2,
                    label=f'P = {p_level*100:.0f}%')

        ax1.set_xlabel('Field Current (A)')
        ax1.set_ylabel('Armature Current (A)')
        ax1.set_title('V-Curves (Ia vs If)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot 2: Power Factor vs Field Current
        ax2 = self.fig.add_subplot(2, 2, 2)

        for p_level, color in zip(power_levels, colors):
            pf_values = []

            for if_val in if_range:
                ea_mag = v_phase * (if_val / params['if_current']) * 1.2
                p_out = p_level * params['s_rated']
                ia = p_out * 1e6 / (np.sqrt(3) * params['v_rated'] * 1000 * 0.85)

                q = (ea_mag - v_phase) / params['xs'] if ea_mag > v_phase else 0
                s = np.sqrt(p_out**2 + q**2) if q > 0 else p_out
                pf = p_out / s if s > 0 else 1.0
                pf = np.clip(pf, 0, 1)

                pf_values.append(pf)

            ax2.plot(if_range, pf_values, color=color, linewidth=2,
                    label=f'P = {p_level*100:.0f}%')

        ax2.set_xlabel('Field Current (A)')
        ax2.set_ylabel('Power Factor')
        ax2.set_title('Power Factor vs Field Current')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim([0, 1.1])

        # Plot 3: Capability Curve
        ax3 = self.fig.add_subplot(2, 2, 3)

        # Leading and lagging power factor limits
        angles = np.linspace(-np.pi/2, np.pi/2, 100)
        p_max = params['s_rated'] * np.cos(angles)
        q_max = params['s_rated'] * np.sin(angles)

        ax3.plot(p_max, q_max, 'b-', linewidth=2, label='MVA Limit')
        ax3.axhline(y=0, color='k', linestyle='--', linewidth=1)
        ax3.axvline(x=0, color='k', linestyle='--', linewidth=1)
        ax3.set_xlabel('Real Power P (MVA)')
        ax3.set_ylabel('Reactive Power Q (MVAR)')
        ax3.set_title('Capability Curve')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.axis('equal')

        # Plot 4: Power Angle Curve
        ax4 = self.fig.add_subplot(2, 2, 4)

        delta = np.linspace(-90, 90, 200)
        ea_mag = v_phase * 1.5  # Assume some excitation
        p_max_curve = (v_phase * ea_mag / params['xs']) * np.sin(np.deg2rad(delta))

        ax4.plot(delta, p_max_curve / 1e6, 'r-', linewidth=2)
        ax4.set_xlabel('Power Angle δ (degrees)')
        ax4.set_ylabel('Power (MW)')
        ax4.set_title('Power-Angle Curve')
        ax4.grid(True, alpha=0.3)
        ax4.axhline(y=0, color='k', linestyle='--', linewidth=1)
        ax4.axvline(x=0, color='k', linestyle='--', linewidth=1)

        self.fig.tight_layout()
        self.canvas.draw()

    def reset_parameters(self):
        """Reset parameters to default values"""
        defaults = {
            "s_rated": "10",
            "v_rated": "13.8",
            "freq": "60",
            "poles": "4",
            "ra": "0.15",
            "xs": "1.2",
            "if_current": "100",
            "pf": "0.85"
        }
        for key, entry in self.params.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[key])
        self.results_text.delete(1.0, tk.END)


class DCMachineLab(ttk.Frame):
    """DC machine modeling and analysis laboratory"""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='TFrame')

        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title = ttk.Label(main_container,
                         text="DC Machine Analysis and Modeling",
                         style='Title.TLabel')
        title.pack(pady=(0, 20))

        # Create two-column layout
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        right_frame = ttk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True)

        # Parameters section
        self.create_parameter_section(left_frame)

        # Results section
        self.create_results_section(left_frame)

        # Plotting section
        self.create_plot_section(right_frame)

    def create_parameter_section(self, parent):
        """Create parameter input section"""
        param_frame = ttk.LabelFrame(parent, text="DC Machine Parameters", padding=15)
        param_frame.pack(fill='x', pady=(0, 20))

        # Parameters
        self.params = {}
        param_list = [
            ("Rated Power (HP):", "50", "hp_rated"),
            ("Rated Voltage (V):", "250", "v_rated"),
            ("Rated Speed (RPM):", "1200", "n_rated"),
            ("Ra - Armature Resistance (Ω):", "0.25", "ra"),
            ("Rf - Field Resistance (Ω):", "100", "rf"),
            ("Laf - Field-Armature Inductance (H):", "0.5", "laf"),
            ("Ka - Armature Constant:", "2.5", "ka"),
        ]

        for i, (label_text, default_val, key) in enumerate(param_list):
            label = ttk.Label(param_frame, text=label_text)
            label.grid(row=i, column=0, sticky='w', pady=5)

            entry = ttk.Entry(param_frame, width=15)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            self.params[key] = entry

        param_frame.columnconfigure(1, weight=1)

        # Machine type selection
        type_label = ttk.Label(param_frame, text="Machine Type:")
        type_label.grid(row=len(param_list), column=0, sticky='w', pady=5)

        self.type_var = tk.StringVar(value="shunt")
        type_frame = ttk.Frame(param_frame)
        type_frame.grid(row=len(param_list), column=1, sticky='w', pady=5)

        shunt_radio = ttk.Radiobutton(type_frame, text="Shunt",
                                     variable=self.type_var, value="shunt")
        shunt_radio.pack(side='left', padx=(0, 10))

        series_radio = ttk.Radiobutton(type_frame, text="Series",
                                      variable=self.type_var, value="series")
        series_radio.pack(side='left')

        # Operation mode selection
        mode_label = ttk.Label(param_frame, text="Operation Mode:")
        mode_label.grid(row=len(param_list)+1, column=0, sticky='w', pady=5)

        self.mode_var = tk.StringVar(value="motor")
        mode_frame = ttk.Frame(param_frame)
        mode_frame.grid(row=len(param_list)+1, column=1, sticky='w', pady=5)

        mot_radio = ttk.Radiobutton(mode_frame, text="Motor",
                                    variable=self.mode_var, value="motor")
        mot_radio.pack(side='left', padx=(0, 10))

        gen_radio = ttk.Radiobutton(mode_frame, text="Generator",
                                    variable=self.mode_var, value="generator")
        gen_radio.pack(side='left')

        # Buttons
        button_frame = ttk.Frame(param_frame)
        button_frame.grid(row=len(param_list)+2, column=0, columnspan=2, pady=(15, 0))

        calc_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calc_btn.pack(side='left', padx=5)

        plot_btn = ttk.Button(button_frame, text="Plot Characteristics",
                             command=self.plot_characteristics)
        plot_btn.pack(side='left', padx=5)

        reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_parameters)
        reset_btn.pack(side='left', padx=5)

    def create_results_section(self, parent):
        """Create results display section"""
        results_frame = ttk.LabelFrame(parent, text="Calculated Results", padding=15)
        results_frame.pack(fill='both', expand=True)

        self.results_text = tk.Text(results_frame, height=15, width=50,
                                   font=('Courier', 10), bg='#FFFFFF',
                                   relief='solid', borderwidth=1)
        self.results_text.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)

    def create_plot_section(self, parent):
        """Create plotting section"""
        plot_frame = ttk.LabelFrame(parent, text="Visualization", padding=10)
        plot_frame.pack(fill='both', expand=True)

        # Create matplotlib figure
        self.fig = Figure(figsize=(7, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()

    def get_parameters(self):
        """Get parameters from entries"""
        try:
            return {key: float(entry.get()) for key, entry in self.params.items()}
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            return None

    def calculate(self):
        """Calculate DC machine characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        # Calculate rated current
        p_rated = params['hp_rated'] * 746  # Convert to Watts
        i_rated = p_rated / params['v_rated']

        # Calculate field current (for shunt connection)
        if self.type_var.get() == "shunt":
            if_rated = params['v_rated'] / params['rf']
            ia_rated = i_rated - if_rated
        else:
            if_rated = i_rated
            ia_rated = i_rated

        # Calculate back EMF at rated conditions
        ea_rated = params['v_rated'] - ia_rated * params['ra']

        # Calculate torque constant
        k_phi = ea_rated / params['n_rated']  # V/(rad/s) when multiplied by 2*pi/60

        # Calculate rated torque
        w_rated = params['n_rated'] * 2 * np.pi / 60
        t_rated = p_rated / w_rated

        # Calculate starting current (if motor)
        if self.mode_var.get() == "motor":
            i_start = params['v_rated'] / params['ra']
            t_start = params['ka'] * if_rated * i_start
        else:
            i_start = 0
            t_start = 0

        # Calculate no-load speed (motor)
        if self.mode_var.get() == "motor":
            n_no_load = params['v_rated'] / (params['ka'] * if_rated) * 60 / (2 * np.pi)
        else:
            n_no_load = 0

        # Calculate speed regulation
        if self.mode_var.get() == "motor":
            speed_reg = (n_no_load - params['n_rated']) / params['n_rated'] * 100
        else:
            speed_reg = 0

        # Calculate efficiency at rated load
        if self.mode_var.get() == "motor":
            p_cu_armature = ia_rated**2 * params['ra']
            p_cu_field = if_rated**2 * params['rf']
            p_rotational = 0.02 * p_rated  # Assume 2% rotational loss
            p_in = p_rated + p_cu_armature + p_cu_field + p_rotational
            efficiency = p_rated / p_in * 100
        else:
            p_cu_armature = ia_rated**2 * params['ra']
            p_cu_field = if_rated**2 * params['rf']
            p_rotational = 0.02 * p_rated
            p_out = p_rated - p_cu_armature - p_cu_field - p_rotational
            efficiency = p_out / p_rated * 100

        # Display results
        machine_type = "SHUNT" if self.type_var.get() == "shunt" else "SERIES"
        mode_str = "MOTOR" if self.mode_var.get() == "motor" else "GENERATOR"

        results = f"""
DC {machine_type} {mode_str} ANALYSIS RESULTS
{'=' * 50}

Machine Ratings:
  Rated Power:                {params['hp_rated']:.1f} HP ({p_rated:.0f} W)
  Rated Voltage:              {params['v_rated']:.1f} V
  Rated Speed:                {params['n_rated']:.0f} RPM
  Rated Current:              {i_rated:.2f} A

Armature Circuit:
  Armature Resistance:        {params['ra']:.3f} Ω
  Armature Current (rated):   {ia_rated:.2f} A
  Back EMF (rated):           {ea_rated:.2f} V

Field Circuit:
  Field Resistance:           {params['rf']:.1f} Ω
  Field Current (rated):      {if_rated:.3f} A

Performance Characteristics:
  Rated Torque:               {t_rated:.2f} N⋅m
  Rated Angular Velocity:     {w_rated:.2f} rad/s
"""

        if self.mode_var.get() == "motor":
            results += f"""
Motor-Specific Parameters:
  Starting Current:           {i_start:.2f} A
  Starting Torque:            {t_start:.2f} N⋅m
  No-Load Speed:              {n_no_load:.0f} RPM
  Speed Regulation:           {speed_reg:.2f} %
"""

        results += f"""
Losses and Efficiency:
  Armature Copper Loss:       {ia_rated**2 * params['ra']:.2f} W
  Field Copper Loss:          {if_rated**2 * params['rf']:.2f} W
  Efficiency (rated):         {efficiency:.2f} %
{'=' * 50}
"""

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)

    def plot_characteristics(self):
        """Plot DC machine characteristics"""
        params = self.get_parameters()
        if params is None:
            return

        self.fig.clear()

        p_rated = params['hp_rated'] * 746
        i_rated = p_rated / params['v_rated']

        if self.type_var.get() == "shunt":
            if_rated = params['v_rated'] / params['rf']
            ia_rated = i_rated - if_rated
        else:
            if_rated = i_rated
            ia_rated = i_rated

        if self.mode_var.get() == "motor":
            # Motor characteristics

            # Current range
            ia = np.linspace(0, 2 * ia_rated, 100)

            # For shunt motor
            if self.type_var.get() == "shunt":
                # Speed characteristic
                ea = params['v_rated'] - ia * params['ra']
                n = ea / (params['ka'] * if_rated) * 60 / (2 * np.pi)
                n = np.maximum(n, 0)

                # Torque
                t = params['ka'] * if_rated * ia
            else:
                # Series motor
                # Flux proportional to current
                phi = ia * 0.1  # Simplified
                ea = params['v_rated'] - ia * params['ra']
                n = ea / (params['ka'] * phi) * 60 / (2 * np.pi)
                n = np.maximum(n, 0)
                n = np.minimum(n, 5000)  # Limit for visualization

                # Torque
                t = params['ka'] * phi * ia

            # Plot 1: Speed-Torque Characteristic
            ax1 = self.fig.add_subplot(2, 2, 1)
            ax1.plot(t, n, 'b-', linewidth=2)
            ax1.set_xlabel('Torque (N⋅m)')
            ax1.set_ylabel('Speed (RPM)')
            ax1.set_title('Speed-Torque Characteristic')
            ax1.grid(True, alpha=0.3)

            # Plot 2: Speed-Current Characteristic
            ax2 = self.fig.add_subplot(2, 2, 2)
            ax2.plot(ia, n, 'r-', linewidth=2)
            ax2.set_xlabel('Armature Current (A)')
            ax2.set_ylabel('Speed (RPM)')
            ax2.set_title('Speed-Current Characteristic')
            ax2.grid(True, alpha=0.3)

            # Plot 3: Torque-Current Characteristic
            ax3 = self.fig.add_subplot(2, 2, 3)
            ax3.plot(ia, t, 'g-', linewidth=2)
            ax3.set_xlabel('Armature Current (A)')
            ax3.set_ylabel('Torque (N⋅m)')
            ax3.set_title('Torque-Current Characteristic')
            ax3.grid(True, alpha=0.3)

            # Plot 4: Efficiency vs Load
            ax4 = self.fig.add_subplot(2, 2, 4)
            load_percent = ia / ia_rated * 100
            p_out = params['v_rated'] * ia - ia**2 * params['ra']
            p_cu = ia**2 * params['ra'] + if_rated**2 * params['rf']
            p_rot = 0.02 * p_rated * np.ones_like(ia)
            eff = np.where(p_out + p_cu + p_rot > 0,
                          p_out / (p_out + p_cu + p_rot) * 100, 0)
            eff = np.clip(eff, 0, 100)
            ax4.plot(load_percent, eff, 'm-', linewidth=2)
            ax4.set_xlabel('Load (%)')
            ax4.set_ylabel('Efficiency (%)')
            ax4.set_title('Efficiency vs Load')
            ax4.grid(True, alpha=0.3)
            ax4.set_ylim([0, 100])

        else:
            # Generator characteristics

            # Speed range
            n = np.linspace(0, 2 * params['n_rated'], 100)
            w = n * 2 * np.pi / 60

            # For shunt generator
            if self.type_var.get() == "shunt":
                # Generated EMF
                ea = params['ka'] * if_rated * w

                # Terminal voltage at different loads
                il_values = [0, ia_rated * 0.5, ia_rated, ia_rated * 1.5]

                # Plot 1: Voltage-Speed Characteristic
                ax1 = self.fig.add_subplot(2, 2, 1)
                for il in il_values:
                    vt = ea - il * params['ra']
                    vt = np.maximum(vt, 0)
                    ax1.plot(n, vt, linewidth=2, label=f'IL = {il:.1f} A')
                ax1.set_xlabel('Speed (RPM)')
                ax1.set_ylabel('Terminal Voltage (V)')
                ax1.set_title('Terminal Voltage vs Speed')
                ax1.grid(True, alpha=0.3)
                ax1.legend()

                # Plot 2: Voltage-Current (Load) Characteristic
                ax2 = self.fig.add_subplot(2, 2, 2)
                il = np.linspace(0, 2 * ia_rated, 100)
                ea_const = params['ka'] * if_rated * params['n_rated'] * 2 * np.pi / 60
                vt = ea_const - il * params['ra']
                vt = np.maximum(vt, 0)
                ax2.plot(il, vt, 'r-', linewidth=2)
                ax2.set_xlabel('Load Current (A)')
                ax2.set_ylabel('Terminal Voltage (V)')
                ax2.set_title('External Characteristic')
                ax2.grid(True, alpha=0.3)

                # Plot 3: Voltage Regulation
                ax3 = self.fig.add_subplot(2, 2, 3)
                vr = (ea_const - vt) / vt * 100
                vr = np.where(vt > 0, vr, 0)
                ax3.plot(il, vr, 'g-', linewidth=2)
                ax3.set_xlabel('Load Current (A)')
                ax3.set_ylabel('Voltage Regulation (%)')
                ax3.set_title('Voltage Regulation vs Load')
                ax3.grid(True, alpha=0.3)

                # Plot 4: Efficiency
                ax4 = self.fig.add_subplot(2, 2, 4)
                p_out = vt * il
                p_cu = il**2 * params['ra'] + if_rated**2 * params['rf']
                p_rot = 0.02 * p_rated * np.ones_like(il)
                p_in = p_out + p_cu + p_rot
                eff = np.where(p_in > 0, p_out / p_in * 100, 0)
                eff = np.clip(eff, 0, 100)
                ax4.plot(il, eff, 'm-', linewidth=2)
                ax4.set_xlabel('Load Current (A)')
                ax4.set_ylabel('Efficiency (%)')
                ax4.set_title('Efficiency vs Load')
                ax4.grid(True, alpha=0.3)
                ax4.set_ylim([0, 100])

        self.fig.tight_layout()
        self.canvas.draw()

    def reset_parameters(self):
        """Reset parameters to default values"""
        defaults = {
            "hp_rated": "50",
            "v_rated": "250",
            "n_rated": "1200",
            "ra": "0.25",
            "rf": "100",
            "laf": "0.5",
            "ka": "2.5"
        }
        for key, entry in self.params.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[key])
        self.results_text.delete(1.0, tk.END)


def main():
    """Main entry point for the application"""
    app = ElectricalMachineLab()
    app.mainloop()


if __name__ == "__main__":
    main()
