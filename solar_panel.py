"""
Solar Panel and Array Model

This module implements models for photovoltaic (PV) panels and arrays:
- Single diode model
- PV panel characteristics
- Series/parallel array configurations
- Environmental effects (temperature, irradiance)

Author: Solar Panel Model Implementation
Date: 2025-11-05
"""

import numpy as np
from typing import Tuple, Optional
import warnings


class SolarPanel:
    """
    Solar Panel Model using Single Diode Equivalent Circuit

    The single diode model represents a PV cell with:
    - Photocurrent source (I_ph)
    - Diode
    - Series resistance (R_s)
    - Shunt/parallel resistance (R_sh)
    """

    def __init__(self,
                 V_oc: float = 37.3,      # Open circuit voltage (V)
                 I_sc: float = 8.51,      # Short circuit current (A)
                 V_mp: float = 30.0,      # Voltage at max power (V)
                 I_mp: float = 7.84,      # Current at max power (A)
                 N_s: int = 60,           # Number of cells in series
                 T_nom: float = 25.0,     # Nominal temperature (°C)
                 G_nom: float = 1000.0,   # Nominal irradiance (W/m²)
                 K_v: float = -0.0032,    # Temperature coefficient for voltage (V/°C)
                 K_i: float = 0.0005,     # Temperature coefficient for current (A/°C)
                 ):
        """
        Initialize Solar Panel Model

        Parameters:
        -----------
        V_oc : float
            Open circuit voltage at STC (V)
        I_sc : float
            Short circuit current at STC (A)
        V_mp : float
            Voltage at maximum power point at STC (V)
        I_mp : float
            Current at maximum power point at STC (A)
        N_s : int
            Number of cells in series
        T_nom : float
            Nominal/reference temperature (°C)
        G_nom : float
            Nominal/reference irradiance (W/m²)
        K_v : float
            Temperature coefficient for voltage (V/°C)
        K_i : float
            Temperature coefficient for current (A/°C)
        """
        self.V_oc = V_oc
        self.I_sc = I_sc
        self.V_mp = V_mp
        self.I_mp = I_mp
        self.P_max = V_mp * I_mp
        self.N_s = N_s
        self.T_nom = T_nom
        self.G_nom = G_nom
        self.K_v = K_v
        self.K_i = K_i

        # Physical constants
        self.q = 1.602176634e-19  # Elementary charge (C)
        self.k = 1.380649e-23      # Boltzmann constant (J/K)
        self.T_nom_K = T_nom + 273.15  # Nominal temperature in Kelvin

        # Calculate model parameters
        self._calculate_parameters()

    def _calculate_parameters(self):
        """Calculate internal model parameters"""
        # Thermal voltage at nominal temperature
        V_t = self.N_s * self.k * self.T_nom_K / self.q

        # Ideality factor (typically 1-2 for silicon)
        self.n = 1.3

        # Series resistance estimation
        self.R_s = 0.221  # Simplified estimation (Ω)

        # Shunt resistance estimation
        self.R_sh = 415.405  # Simplified estimation (Ω)

        # Reverse saturation current
        self.I_0 = self.I_sc / (np.exp(self.V_oc / (self.n * V_t)) - 1)

        # Photocurrent at STC
        self.I_ph_nom = self.I_sc

    def get_current(self, voltage: float, temperature: float = 25.0,
                    irradiance: float = 1000.0) -> float:
        """
        Calculate panel current for given voltage and environmental conditions

        Uses the single diode equation:
        I = I_ph - I_0 * (exp((V + I*R_s)/(n*V_t)) - 1) - (V + I*R_s)/R_sh

        Parameters:
        -----------
        voltage : float
            Panel terminal voltage (V)
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        float
            Panel current (A)
        """
        # Temperature in Kelvin
        T_K = temperature + 273.15

        # Thermal voltage
        V_t = self.N_s * self.k * T_K / self.q

        # Photocurrent (scales with irradiance and temperature)
        dT = temperature - self.T_nom
        I_ph = (self.I_ph_nom + self.K_i * dT) * (irradiance / self.G_nom)

        # Reverse saturation current (temperature dependent)
        I_0 = self.I_0 * (T_K / self.T_nom_K) ** 3 * \
              np.exp(self.q * 1.12 / (self.n * self.k) * (1 / self.T_nom_K - 1 / T_K))

        # Solve for current iteratively (Newton-Raphson method)
        I = I_ph  # Initial guess

        for _ in range(50):  # Maximum iterations
            # Current equation
            f = I_ph - I - I_0 * (np.exp((voltage + I * self.R_s) / (self.n * V_t)) - 1) - \
                (voltage + I * self.R_s) / self.R_sh

            # Derivative
            df = -1 - I_0 * self.R_s / (self.n * V_t) * \
                 np.exp((voltage + I * self.R_s) / (self.n * V_t)) - self.R_s / self.R_sh

            # Newton-Raphson update
            I_new = I - f / df

            # Check convergence
            if abs(I_new - I) < 1e-6:
                I = I_new
                break

            I = I_new

        return max(0, I)  # Current cannot be negative

    def get_power(self, voltage: float, temperature: float = 25.0,
                  irradiance: float = 1000.0) -> float:
        """
        Calculate panel power output

        Parameters:
        -----------
        voltage : float
            Panel terminal voltage (V)
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        float
            Panel power (W)
        """
        current = self.get_current(voltage, temperature, irradiance)
        return voltage * current

    def get_iv_curve(self, temperature: float = 25.0, irradiance: float = 1000.0,
                     num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate I-V characteristic curve

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)
        num_points : int
            Number of points in the curve

        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Voltage array (V) and Current array (A)
        """
        voltages = np.linspace(0, self.V_oc * 1.1, num_points)
        currents = np.array([self.get_current(v, temperature, irradiance)
                            for v in voltages])
        return voltages, currents

    def get_pv_curve(self, temperature: float = 25.0, irradiance: float = 1000.0,
                     num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate P-V characteristic curve

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)
        num_points : int
            Number of points in the curve

        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Voltage array (V) and Power array (W)
        """
        voltages, currents = self.get_iv_curve(temperature, irradiance, num_points)
        powers = voltages * currents
        return voltages, powers

    def find_mpp(self, temperature: float = 25.0, irradiance: float = 1000.0) -> Tuple[float, float, float]:
        """
        Find the Maximum Power Point

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        Tuple[float, float, float]
            MPP voltage (V), MPP current (A), MPP power (W)
        """
        voltages, powers = self.get_pv_curve(temperature, irradiance, 200)
        mpp_idx = np.argmax(powers)
        v_mpp = voltages[mpp_idx]
        p_mpp = powers[mpp_idx]
        i_mpp = self.get_current(v_mpp, temperature, irradiance)

        return v_mpp, i_mpp, p_mpp


class SolarArray:
    """
    Solar Array Model - Series and Parallel configuration of panels
    """

    def __init__(self, panel: SolarPanel, N_series: int = 1, N_parallel: int = 1):
        """
        Initialize Solar Array

        Parameters:
        -----------
        panel : SolarPanel
            Base solar panel model
        N_series : int
            Number of panels in series
        N_parallel : int
            Number of panels in parallel
        """
        self.panel = panel
        self.N_series = N_series
        self.N_parallel = N_parallel

        # Array characteristics
        self.V_oc = panel.V_oc * N_series
        self.I_sc = panel.I_sc * N_parallel
        self.V_mp = panel.V_mp * N_series
        self.I_mp = panel.I_mp * N_parallel
        self.P_max = panel.P_max * N_series * N_parallel

    def get_current(self, voltage: float, temperature: float = 25.0,
                    irradiance: float = 1000.0) -> float:
        """
        Calculate array current

        Parameters:
        -----------
        voltage : float
            Array terminal voltage (V)
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        float
            Array current (A)
        """
        # Voltage per panel in series string
        v_panel = voltage / self.N_series

        # Current from one series string
        i_string = self.panel.get_current(v_panel, temperature, irradiance)

        # Total array current (parallel strings)
        return i_string * self.N_parallel

    def get_power(self, voltage: float, temperature: float = 25.0,
                  irradiance: float = 1000.0) -> float:
        """
        Calculate array power output

        Parameters:
        -----------
        voltage : float
            Array terminal voltage (V)
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        float
            Array power (W)
        """
        current = self.get_current(voltage, temperature, irradiance)
        return voltage * current

    def get_iv_curve(self, temperature: float = 25.0, irradiance: float = 1000.0,
                     num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate array I-V characteristic curve

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)
        num_points : int
            Number of points in the curve

        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Voltage array (V) and Current array (A)
        """
        voltages = np.linspace(0, self.V_oc * 1.1, num_points)
        currents = np.array([self.get_current(v, temperature, irradiance)
                            for v in voltages])
        return voltages, currents

    def get_pv_curve(self, temperature: float = 25.0, irradiance: float = 1000.0,
                     num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate array P-V characteristic curve

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)
        num_points : int
            Number of points in the curve

        Returns:
        --------
        Tuple[np.ndarray, np.ndarray]
            Voltage array (V) and Power array (W)
        """
        voltages, currents = self.get_iv_curve(temperature, irradiance, num_points)
        powers = voltages * currents
        return voltages, powers

    def find_mpp(self, temperature: float = 25.0, irradiance: float = 1000.0) -> Tuple[float, float, float]:
        """
        Find the Maximum Power Point of the array

        Parameters:
        -----------
        temperature : float
            Cell temperature (°C)
        irradiance : float
            Solar irradiance (W/m²)

        Returns:
        --------
        Tuple[float, float, float]
            MPP voltage (V), MPP current (A), MPP power (W)
        """
        voltages, powers = self.get_pv_curve(temperature, irradiance, 200)
        mpp_idx = np.argmax(powers)
        v_mpp = voltages[mpp_idx]
        p_mpp = powers[mpp_idx]
        i_mpp = self.get_current(v_mpp, temperature, irradiance)

        return v_mpp, i_mpp, p_mpp


def create_standard_panel(panel_type: str = 'generic') -> SolarPanel:
    """
    Factory function to create standard panel types

    Parameters:
    -----------
    panel_type : str
        Type of panel: 'generic', 'canadian_solar_cs6k', 'sunpower_e20'

    Returns:
    --------
    SolarPanel
        Configured solar panel instance
    """
    panels = {
        'generic': {
            'V_oc': 37.3,
            'I_sc': 8.51,
            'V_mp': 30.0,
            'I_mp': 7.84,
            'N_s': 60
        },
        'canadian_solar_cs6k': {
            'V_oc': 45.6,
            'I_sc': 8.83,
            'V_mp': 37.0,
            'I_mp': 8.31,
            'N_s': 72
        },
        'sunpower_e20': {
            'V_oc': 67.8,
            'I_sc': 5.35,
            'V_mp': 57.3,
            'I_mp': 5.10,
            'N_s': 96
        }
    }

    if panel_type not in panels:
        warnings.warn(f"Unknown panel type: {panel_type}. Using 'generic'.")
        panel_type = 'generic'

    return SolarPanel(**panels[panel_type])


if __name__ == "__main__":
    # Example usage
    print("Solar Panel Model")
    print("=" * 50)

    # Create a solar panel
    panel = create_standard_panel('generic')

    # Find MPP at STC
    v_mpp, i_mpp, p_mpp = panel.find_mpp(25.0, 1000.0)
    print(f"\nMaximum Power Point at STC:")
    print(f"  Voltage: {v_mpp:.2f} V")
    print(f"  Current: {i_mpp:.2f} A")
    print(f"  Power: {p_mpp:.2f} W")

    # Create a solar array (4 series, 3 parallel)
    array = SolarArray(panel, N_series=4, N_parallel=3)
    v_mpp, i_mpp, p_mpp = array.find_mpp(25.0, 1000.0)
    print(f"\nSolar Array (4S x 3P) MPP at STC:")
    print(f"  Voltage: {v_mpp:.2f} V")
    print(f"  Current: {i_mpp:.2f} A")
    print(f"  Power: {p_mpp:.2f} W")
