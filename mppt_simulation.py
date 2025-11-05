"""
MPPT Simulation and Demonstration

This script demonstrates the MPPT controller with solar panel models.
It simulates various conditions and compares different MPPT algorithms.

Author: MPPT Simulation
Date: 2025-11-05
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mppt_controller import create_mppt_controller, PerturbAndObserve, IncrementalConductance
from solar_panel import SolarPanel, SolarArray, create_standard_panel


class BoostConverter:
    """
    Simple Boost Converter Model for MPPT system

    Vout = Vin / (1 - D)
    where D is the duty cycle
    """

    def __init__(self, V_out: float = 48.0, efficiency: float = 0.95):
        """
        Initialize Boost Converter

        Parameters:
        -----------
        V_out : float
            Output voltage (V)
        efficiency : float
            Converter efficiency (0-1)
        """
        self.V_out = V_out
        self.efficiency = efficiency

    def get_input_voltage(self, duty_cycle: float, v_array: float) -> float:
        """
        Calculate input voltage based on duty cycle

        For MPPT simulation, we model the relationship between
        duty cycle and operating point on the PV curve

        Parameters:
        -----------
        duty_cycle : float
            Duty cycle (0-1)
        v_array : float
            Array open circuit voltage

        Returns:
        --------
        float
            Operating voltage (V)
        """
        # Simplified model: duty cycle controls operating voltage
        # D = 0.5 -> V_operating ≈ V_mpp
        # Lower D -> higher voltage, Higher D -> lower voltage
        v_operating = v_array * (1 - duty_cycle) * 1.8
        return v_operating


class MPPTSimulator:
    """MPPT System Simulator"""

    def __init__(self, panel: SolarPanel, mppt_algorithm: str = 'P&O',
                 load_voltage: float = 48.0):
        """
        Initialize MPPT Simulator

        Parameters:
        -----------
        panel : SolarPanel
            Solar panel model
        mppt_algorithm : str
            MPPT algorithm to use
        load_voltage : float
            Load/battery voltage (V)
        """
        self.panel = panel
        self.converter = BoostConverter(V_out=load_voltage)

        # Create MPPT controller
        if mppt_algorithm == 'P&O':
            self.mppt = create_mppt_controller('P&O', step_size=0.005)
        elif mppt_algorithm == 'InCond':
            self.mppt = create_mppt_controller('InCond', step_size=0.005)
        elif mppt_algorithm == 'CV':
            v_mpp, _, _ = panel.find_mpp()
            self.mppt = create_mppt_controller('CV', v_ref=v_mpp)
        else:
            self.mppt = create_mppt_controller(mppt_algorithm)

        self.algorithm = mppt_algorithm

        # Simulation state
        self.time = []
        self.voltage_history = []
        self.current_history = []
        self.power_history = []
        self.duty_cycle_history = []
        self.efficiency_history = []

    def simulate_step(self, temperature: float, irradiance: float) -> dict:
        """
        Simulate one time step

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        dict
            Simulation results for this step
        """
        # Get operating voltage from duty cycle
        v_operating = self.converter.get_input_voltage(
            self.mppt.duty_cycle, self.panel.V_oc
        )

        # Get current and power from panel
        current = self.panel.get_current(v_operating, temperature, irradiance)
        power = v_operating * current

        # Update MPPT controller
        duty_cycle = self.mppt.update(v_operating, current)

        # Calculate tracking efficiency
        _, _, p_mpp = self.panel.find_mpp(temperature, irradiance)
        efficiency = (power / p_mpp * 100) if p_mpp > 0 else 0

        return {
            'voltage': v_operating,
            'current': current,
            'power': power,
            'duty_cycle': duty_cycle,
            'efficiency': efficiency,
            'p_mpp': p_mpp
        }

    def run_simulation(self, duration: float = 10.0, dt: float = 0.01,
                      temperature: float = 25.0, irradiance: float = 1000.0,
                      variable_conditions: bool = False):
        """
        Run MPPT simulation

        Parameters:
        -----------
        duration : float
            Simulation duration (seconds)
        dt : float
            Time step (seconds)
        temperature : float or callable
            Temperature (°C) - can be constant or function of time
        irradiance : float or callable
            Irradiance (W/m²) - can be constant or function of time
        variable_conditions : bool
            Use variable environmental conditions
        """
        # Reset simulation
        self.mppt.reset()
        self.time = []
        self.voltage_history = []
        self.current_history = []
        self.power_history = []
        self.duty_cycle_history = []
        self.efficiency_history = []

        # Run simulation
        t = 0
        while t <= duration:
            # Get environmental conditions
            if variable_conditions:
                # Simulate varying irradiance (cloud passing)
                G = 1000.0 * (0.7 + 0.3 * np.sin(2 * np.pi * t / 5.0))
                # Simulate varying temperature
                T = 25.0 + 10.0 * np.sin(2 * np.pi * t / 20.0)
            else:
                if callable(temperature):
                    T = temperature(t)
                else:
                    T = temperature

                if callable(irradiance):
                    G = irradiance(t)
                else:
                    G = irradiance

            # Simulate one step
            result = self.simulate_step(T, G)

            # Store results
            self.time.append(t)
            self.voltage_history.append(result['voltage'])
            self.current_history.append(result['current'])
            self.power_history.append(result['power'])
            self.duty_cycle_history.append(result['duty_cycle'])
            self.efficiency_history.append(result['efficiency'])

            t += dt

        # Convert to numpy arrays
        self.time = np.array(self.time)
        self.voltage_history = np.array(self.voltage_history)
        self.current_history = np.array(self.current_history)
        self.power_history = np.array(self.power_history)
        self.duty_cycle_history = np.array(self.duty_cycle_history)
        self.efficiency_history = np.array(self.efficiency_history)

    def plot_results(self, save_path: str = None):
        """
        Plot simulation results

        Parameters:
        -----------
        save_path : str, optional
            Path to save the plot
        """
        fig = plt.figure(figsize=(14, 10))
        gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

        # Voltage
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(self.time, self.voltage_history, 'b-', linewidth=2)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Voltage (V)')
        ax1.set_title('PV Voltage')
        ax1.grid(True, alpha=0.3)

        # Current
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(self.time, self.current_history, 'r-', linewidth=2)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Current (A)')
        ax2.set_title('PV Current')
        ax2.grid(True, alpha=0.3)

        # Power
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.plot(self.time, self.power_history, 'g-', linewidth=2)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Power (W)')
        ax3.set_title('PV Power')
        ax3.grid(True, alpha=0.3)

        # Duty Cycle
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.plot(self.time, self.duty_cycle_history, 'm-', linewidth=2)
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Duty Cycle')
        ax4.set_title('MPPT Duty Cycle')
        ax4.grid(True, alpha=0.3)

        # Efficiency
        ax5 = fig.add_subplot(gs[2, :])
        ax5.plot(self.time, self.efficiency_history, 'c-', linewidth=2)
        ax5.set_xlabel('Time (s)')
        ax5.set_ylabel('Tracking Efficiency (%)')
        ax5.set_title(f'MPPT Tracking Efficiency ({self.algorithm})')
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim([0, 105])

        fig.suptitle(f'MPPT Simulation Results - {self.algorithm} Algorithm',
                    fontsize=16, fontweight='bold')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")

        plt.show()

        # Print statistics
        print(f"\n{self.algorithm} Algorithm Performance:")
        print(f"  Average Power: {np.mean(self.power_history):.2f} W")
        print(f"  Average Efficiency: {np.mean(self.efficiency_history):.2f}%")
        print(f"  Min Efficiency: {np.min(self.efficiency_history):.2f}%")
        print(f"  Max Efficiency: {np.max(self.efficiency_history):.2f}%")


def compare_algorithms():
    """Compare different MPPT algorithms"""
    print("Comparing MPPT Algorithms")
    print("=" * 50)

    # Create solar panel
    panel = create_standard_panel('generic')

    algorithms = ['P&O', 'InCond']
    colors = ['b', 'r', 'g', 'm']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('MPPT Algorithm Comparison', fontsize=16, fontweight='bold')

    results = {}

    for i, algo in enumerate(algorithms):
        print(f"\nSimulating {algo} algorithm...")
        sim = MPPTSimulator(panel, mppt_algorithm=algo)
        sim.run_simulation(duration=5.0, dt=0.01, variable_conditions=True)
        results[algo] = sim

    # Plot comparisons
    # Power
    ax1 = axes[0, 0]
    for i, algo in enumerate(algorithms):
        ax1.plot(results[algo].time, results[algo].power_history,
                color=colors[i], linewidth=2, label=algo)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Power (W)')
    ax1.set_title('Power Tracking')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Efficiency
    ax2 = axes[0, 1]
    for i, algo in enumerate(algorithms):
        ax2.plot(results[algo].time, results[algo].efficiency_history,
                color=colors[i], linewidth=2, label=algo)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Efficiency (%)')
    ax2.set_title('Tracking Efficiency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 105])

    # Voltage
    ax3 = axes[1, 0]
    for i, algo in enumerate(algorithms):
        ax3.plot(results[algo].time, results[algo].voltage_history,
                color=colors[i], linewidth=2, label=algo)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Voltage (V)')
    ax3.set_title('Operating Voltage')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Duty Cycle
    ax4 = axes[1, 1]
    for i, algo in enumerate(algorithms):
        ax4.plot(results[algo].time, results[algo].duty_cycle_history,
                color=colors[i], linewidth=2, label=algo)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Duty Cycle')
    ax4.set_title('Control Signal')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/Chapman/mppt_comparison.png', dpi=300, bbox_inches='tight')
    print("\nComparison plot saved to mppt_comparison.png")
    plt.show()

    # Print comparison statistics
    print("\n" + "=" * 50)
    print("Algorithm Performance Comparison:")
    print("=" * 50)
    for algo in algorithms:
        print(f"\n{algo}:")
        print(f"  Avg Power: {np.mean(results[algo].power_history):.2f} W")
        print(f"  Avg Efficiency: {np.mean(results[algo].efficiency_history):.2f}%")


def demo_pv_characteristics():
    """Demonstrate PV panel characteristics"""
    print("\nDemonstrating PV Panel Characteristics")
    print("=" * 50)

    panel = create_standard_panel('generic')

    # Different conditions
    conditions = [
        (25, 1000, 'STC: 25°C, 1000 W/m²'),
        (25, 800, '25°C, 800 W/m²'),
        (25, 600, '25°C, 600 W/m²'),
        (50, 1000, '50°C, 1000 W/m²'),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    for temp, irrad, label in conditions:
        # I-V curve
        V, I = panel.get_iv_curve(temp, irrad)
        ax1.plot(V, I, linewidth=2, label=label)

        # P-V curve
        V, P = panel.get_pv_curve(temp, irrad)
        ax2.plot(V, P, linewidth=2, label=label)

        # Mark MPP
        v_mpp, i_mpp, p_mpp = panel.find_mpp(temp, irrad)
        ax1.plot(v_mpp, i_mpp, 'o', markersize=8)
        ax2.plot(v_mpp, p_mpp, 'o', markersize=8)

    ax1.set_xlabel('Voltage (V)')
    ax1.set_ylabel('Current (A)')
    ax1.set_title('I-V Characteristics')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.set_xlabel('Voltage (V)')
    ax2.set_ylabel('Power (W)')
    ax2.set_title('P-V Characteristics')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/Chapman/pv_characteristics.png', dpi=300, bbox_inches='tight')
    print("PV characteristics plot saved to pv_characteristics.png")
    plt.show()


if __name__ == "__main__":
    print("MPPT Simulation and Demonstration")
    print("=" * 70)

    # Demo 1: PV Characteristics
    demo_pv_characteristics()

    # Demo 2: Single algorithm simulation
    print("\n" + "=" * 70)
    print("Demo: P&O Algorithm Simulation")
    print("=" * 70)
    panel = create_standard_panel('generic')
    sim = MPPTSimulator(panel, mppt_algorithm='P&O')
    sim.run_simulation(duration=5.0, dt=0.01, variable_conditions=True)
    sim.plot_results(save_path='/home/user/Chapman/mppt_po_simulation.png')

    # Demo 3: Algorithm comparison
    print("\n" + "=" * 70)
    print("Demo: Algorithm Comparison")
    print("=" * 70)
    compare_algorithms()

    print("\n" + "=" * 70)
    print("Simulation Complete!")
    print("=" * 70)
