"""
MPPT (Maximum Power Point Tracking) Controller for Photovoltaic Systems

This module implements various MPPT algorithms for solar panel systems:
- Perturb and Observe (P&O)
- Incremental Conductance (InCond)
- Constant Voltage (CV)

Author: MPPT Controller Implementation
Date: 2025-11-05
"""

import numpy as np
from typing import Tuple, Optional


class MPPTController:
    """Base class for MPPT controllers"""

    def __init__(self, algorithm: str = 'P&O'):
        """
        Initialize MPPT Controller

        Parameters:
        -----------
        algorithm : str
            MPPT algorithm to use ('P&O', 'InCond', 'CV')
        """
        self.algorithm = algorithm
        self.v_prev = 0.0
        self.p_prev = 0.0
        self.i_prev = 0.0
        self.duty_cycle = 0.5  # Initial duty cycle (50%)
        self.v_ref = 0.0

    def reset(self):
        """Reset controller state"""
        self.v_prev = 0.0
        self.p_prev = 0.0
        self.i_prev = 0.0
        self.duty_cycle = 0.5


class PerturbAndObserve(MPPTController):
    """
    Perturb and Observe (P&O) MPPT Algorithm

    The P&O algorithm works by:
    1. Measuring voltage and power
    2. Comparing with previous values
    3. Adjusting duty cycle based on power change direction
    """

    def __init__(self, step_size: float = 0.01, v_max: float = 50.0, v_min: float = 10.0):
        """
        Initialize P&O controller

        Parameters:
        -----------
        step_size : float
            Perturbation step size (duty cycle change)
        v_max : float
            Maximum voltage limit (V)
        v_min : float
            Minimum voltage limit (V)
        """
        super().__init__('P&O')
        self.step_size = step_size
        self.v_max = v_max
        self.v_min = v_min

    def update(self, voltage: float, current: float) -> float:
        """
        Update duty cycle based on P&O algorithm

        Parameters:
        -----------
        voltage : float
            Current PV voltage (V)
        current : float
            Current PV current (A)

        Returns:
        --------
        float
            Updated duty cycle (0-1)
        """
        power = voltage * current

        # Calculate changes
        dP = power - self.p_prev
        dV = voltage - self.v_prev

        # P&O algorithm logic
        if dP != 0:
            if dP > 0:
                # Power increased
                if dV > 0:
                    # Voltage increased -> move in same direction
                    self.duty_cycle += self.step_size
                else:
                    # Voltage decreased -> reverse direction
                    self.duty_cycle -= self.step_size
            else:
                # Power decreased
                if dV > 0:
                    # Voltage increased -> reverse direction
                    self.duty_cycle -= self.step_size
                else:
                    # Voltage decreased -> move in same direction
                    self.duty_cycle += self.step_size

        # Limit duty cycle
        self.duty_cycle = np.clip(self.duty_cycle, 0.1, 0.9)

        # Update previous values
        self.v_prev = voltage
        self.p_prev = power

        return self.duty_cycle


class IncrementalConductance(MPPTController):
    """
    Incremental Conductance (InCond) MPPT Algorithm

    The InCond algorithm uses the relationship:
    - At MPP: dI/dV = -I/V
    - Left of MPP: dI/dV > -I/V
    - Right of MPP: dI/dV < -I/V
    """

    def __init__(self, step_size: float = 0.01, tolerance: float = 1e-3):
        """
        Initialize Incremental Conductance controller

        Parameters:
        -----------
        step_size : float
            Step size for duty cycle adjustment
        tolerance : float
            Tolerance for MPP detection
        """
        super().__init__('InCond')
        self.step_size = step_size
        self.tolerance = tolerance

    def update(self, voltage: float, current: float) -> float:
        """
        Update duty cycle based on Incremental Conductance algorithm

        Parameters:
        -----------
        voltage : float
            Current PV voltage (V)
        current : float
            Current PV current (A)

        Returns:
        --------
        float
            Updated duty cycle (0-1)
        """
        # Calculate changes
        dV = voltage - self.v_prev
        dI = current - self.i_prev

        # Avoid division by zero
        if abs(dV) < 1e-6:
            dV = 1e-6

        # Calculate conductances
        inc_cond = dI / dV  # Incremental conductance
        inst_cond = -current / voltage if voltage != 0 else 0  # Instantaneous conductance

        # InCond algorithm logic
        if abs(inc_cond - inst_cond) < self.tolerance:
            # At MPP - no change
            pass
        elif inc_cond > inst_cond:
            # Left of MPP - increase voltage (decrease duty cycle for boost converter)
            self.duty_cycle -= self.step_size
        else:
            # Right of MPP - decrease voltage (increase duty cycle)
            self.duty_cycle += self.step_size

        # Limit duty cycle
        self.duty_cycle = np.clip(self.duty_cycle, 0.1, 0.9)

        # Update previous values
        self.v_prev = voltage
        self.i_prev = current

        return self.duty_cycle


class ConstantVoltage(MPPTController):
    """
    Constant Voltage (CV) MPPT Algorithm

    Simple algorithm that maintains voltage at a fixed percentage
    of open-circuit voltage (typically 76-78% of Voc)
    """

    def __init__(self, v_ref: float = None, v_oc: float = None, ratio: float = 0.76):
        """
        Initialize Constant Voltage controller

        Parameters:
        -----------
        v_ref : float, optional
            Reference voltage (V)
        v_oc : float, optional
            Open circuit voltage (V)
        ratio : float
            Ratio of Voc to use as reference (default 0.76)
        """
        super().__init__('CV')

        if v_ref is not None:
            self.v_ref = v_ref
        elif v_oc is not None:
            self.v_ref = v_oc * ratio
        else:
            raise ValueError("Either v_ref or v_oc must be provided")

        self.Kp = 0.05  # Proportional gain for voltage regulation

    def update(self, voltage: float, current: float) -> float:
        """
        Update duty cycle to maintain constant voltage

        Parameters:
        -----------
        voltage : float
            Current PV voltage (V)
        current : float
            Current PV current (A)

        Returns:
        --------
        float
            Updated duty cycle (0-1)
        """
        # Simple proportional controller
        error = self.v_ref - voltage
        self.duty_cycle += self.Kp * error

        # Limit duty cycle
        self.duty_cycle = np.clip(self.duty_cycle, 0.1, 0.9)

        return self.duty_cycle


class FuzzyLogicMPPT(MPPTController):
    """
    Fuzzy Logic MPPT Algorithm

    Uses fuzzy logic to determine the optimal duty cycle adjustment
    based on error (E) and change in error (CE)
    """

    def __init__(self, step_size: float = 0.01):
        """
        Initialize Fuzzy Logic MPPT controller

        Parameters:
        -----------
        step_size : float
            Base step size for adjustments
        """
        super().__init__('Fuzzy')
        self.step_size = step_size

    def fuzzy_membership(self, x: float) -> dict:
        """
        Calculate fuzzy membership values

        Parameters:
        -----------
        x : float
            Input value

        Returns:
        --------
        dict
            Membership values for each fuzzy set
        """
        memberships = {}

        # Define membership functions (triangular)
        if x < -0.5:
            memberships['NB'] = 1.0  # Negative Big
            memberships['NS'] = 0.0
            memberships['ZE'] = 0.0
            memberships['PS'] = 0.0
            memberships['PB'] = 0.0
        elif x < -0.1:
            memberships['NB'] = (-0.1 - x) / 0.4
            memberships['NS'] = (x + 0.5) / 0.4
            memberships['ZE'] = 0.0
            memberships['PS'] = 0.0
            memberships['PB'] = 0.0
        elif x < 0.1:
            memberships['NB'] = 0.0
            memberships['NS'] = (0.1 - x) / 0.2
            memberships['ZE'] = 1.0 - abs(x) / 0.1
            memberships['PS'] = (x + 0.1) / 0.2
            memberships['PB'] = 0.0
        elif x < 0.5:
            memberships['NB'] = 0.0
            memberships['NS'] = 0.0
            memberships['ZE'] = 0.0
            memberships['PS'] = (0.5 - x) / 0.4
            memberships['PB'] = (x - 0.1) / 0.4
        else:
            memberships['NB'] = 0.0
            memberships['NS'] = 0.0
            memberships['ZE'] = 0.0
            memberships['PS'] = 0.0
            memberships['PB'] = 1.0

        return memberships

    def fuzzy_inference(self, E: float, CE: float) -> float:
        """
        Fuzzy inference for duty cycle change

        Parameters:
        -----------
        E : float
            Error (normalized dP/dV)
        CE : float
            Change in error

        Returns:
        --------
        float
            Duty cycle change
        """
        # Get memberships
        E_memberships = self.fuzzy_membership(E)
        CE_memberships = self.fuzzy_membership(CE)

        # Simplified rule base (example)
        output = 0.0
        total_weight = 0.0

        # Rule: If E is ZE and CE is ZE, then output is ZE
        weight = min(E_memberships.get('ZE', 0), CE_memberships.get('ZE', 0))
        output += weight * 0.0
        total_weight += weight

        # Rule: If E is PS and CE is PS, then output is PB
        weight = min(E_memberships.get('PS', 0), CE_memberships.get('PS', 0))
        output += weight * self.step_size * 2
        total_weight += weight

        # Rule: If E is NS and CE is NS, then output is NB
        weight = min(E_memberships.get('NS', 0), CE_memberships.get('NS', 0))
        output += weight * (-self.step_size * 2)
        total_weight += weight

        # Defuzzification
        if total_weight > 0:
            return output / total_weight
        else:
            return 0.0

    def update(self, voltage: float, current: float) -> float:
        """
        Update duty cycle using fuzzy logic

        Parameters:
        -----------
        voltage : float
            Current PV voltage (V)
        current : float
            Current PV current (A)

        Returns:
        --------
        float
            Updated duty cycle (0-1)
        """
        power = voltage * current

        # Calculate normalized error and change in error
        dP = power - self.p_prev
        dV = voltage - self.v_prev

        E = dP / (dV + 1e-6) if abs(dV) > 1e-6 else 0
        CE = E - (self.p_prev / (self.v_prev + 1e-6))

        # Normalize
        E = np.clip(E / 100, -1, 1)
        CE = np.clip(CE / 100, -1, 1)

        # Get duty cycle change from fuzzy inference
        delta_D = self.fuzzy_inference(E, CE)

        # Update duty cycle
        self.duty_cycle += delta_D
        self.duty_cycle = np.clip(self.duty_cycle, 0.1, 0.9)

        # Update previous values
        self.v_prev = voltage
        self.p_prev = power

        return self.duty_cycle


def create_mppt_controller(algorithm: str = 'P&O', **kwargs) -> MPPTController:
    """
    Factory function to create MPPT controller

    Parameters:
    -----------
    algorithm : str
        Algorithm type: 'P&O', 'InCond', 'CV', 'Fuzzy'
    **kwargs
        Additional parameters for specific algorithms

    Returns:
    --------
    MPPTController
        Configured MPPT controller instance
    """
    algorithms = {
        'P&O': PerturbAndObserve,
        'InCond': IncrementalConductance,
        'CV': ConstantVoltage,
        'Fuzzy': FuzzyLogicMPPT
    }

    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}. Available: {list(algorithms.keys())}")

    return algorithms[algorithm](**kwargs)


if __name__ == "__main__":
    # Example usage
    print("MPPT Controller Module")
    print("=" * 50)
    print("\nAvailable algorithms:")
    print("- Perturb and Observe (P&O)")
    print("- Incremental Conductance (InCond)")
    print("- Constant Voltage (CV)")
    print("- Fuzzy Logic (Fuzzy)")
    print("\nExample:")
    print("  mppt = create_mppt_controller('P&O', step_size=0.01)")
    print("  duty_cycle = mppt.update(voltage, current)")
