"""
Direct Torque Control (DTC) Controller
Hysteresis-based direct torque control for AC motors
"""

import numpy as np


class DTCController:
    """
    Direct Torque Control

    Implements DTC with:
    - Torque hysteresis control
    - Flux hysteresis control
    - Optimal switching table
    - Sector determination
    """

    def __init__(self, flux_ref=0.8, torque_hyst=0.1, flux_hyst=0.02, Vdc=400):
        """
        Initialize DTC controller

        Parameters:
        -----------
        flux_ref : float
            Reference flux magnitude (Wb)
        torque_hyst : float
            Torque hysteresis band
        flux_hyst : float
            Flux hysteresis band
        Vdc : float
            DC bus voltage
        """
        self.flux_ref = flux_ref
        self.torque_hyst = torque_hyst
        self.flux_hyst = flux_hyst
        self.Vdc = Vdc

        # Internal states
        self.torque_flag = 0  # -1, 0, 1
        self.flux_flag = 0    # -1, 0, 1
        self.sector = 0       # 1-6

        # Switching table for voltage vector selection
        # Row: flux flag, Column: torque flag, 3rd dimension: sector
        self.switching_table = self._initialize_switching_table()

        # Voltage vectors (alpha-beta components)
        self.voltage_vectors = self._initialize_voltage_vectors()

    def _initialize_voltage_vectors(self):
        """
        Initialize space vector voltage table

        Returns 8 voltage vectors (including zero vectors)
        """
        V_base = 2.0 * self.Vdc / 3.0

        vectors = []
        # V0: zero vector
        vectors.append([0, 0])

        # V1-V6: active vectors
        for i in range(6):
            angle = i * np.pi / 3
            vectors.append([V_base * np.cos(angle), V_base * np.sin(angle)])

        # V7: zero vector
        vectors.append([0, 0])

        return np.array(vectors)

    def _initialize_switching_table(self):
        """
        Initialize optimal switching table for DTC

        Table dimensions: [flux_flag+1][torque_flag+1][sector-1]
        flux_flag: -1 (decrease), 0 (maintain), 1 (increase)
        torque_flag: -1 (decrease), 0 (maintain), 1 (increase)
        sector: 1-6
        """
        # Simplified switching table
        # Returns voltage vector index (0-7)
        table = np.zeros((3, 3, 6), dtype=int)

        # When flux needs to increase (flux_flag = 1)
        table[2, 2, :] = [2, 3, 4, 5, 6, 1]  # Increase torque
        table[2, 1, :] = [0, 0, 0, 0, 0, 0]  # Maintain torque
        table[2, 0, :] = [6, 1, 2, 3, 4, 5]  # Decrease torque

        # When flux needs to decrease (flux_flag = -1)
        table[0, 2, :] = [3, 4, 5, 6, 1, 2]  # Increase torque
        table[0, 1, :] = [7, 7, 7, 7, 7, 7]  # Maintain torque
        table[0, 0, :] = [5, 6, 1, 2, 3, 4]  # Decrease torque

        # When flux is OK (flux_flag = 0)
        table[1, 2, :] = [2, 3, 4, 5, 6, 1]  # Increase torque
        table[1, 1, :] = [0, 0, 0, 0, 0, 0]  # Maintain torque
        table[1, 0, :] = [6, 1, 2, 3, 4, 5]  # Decrease torque

        return table

    def estimate_flux(self, v_alpha, v_beta, i_alpha, i_beta, Rs, dt):
        """
        Estimate stator flux linkage using voltage model

        Parameters:
        -----------
        v_alpha, v_beta : float
            Stator voltages in alpha-beta frame
        i_alpha, i_beta : float
            Stator currents in alpha-beta frame
        Rs : float
            Stator resistance
        dt : float
            Time step

        Returns:
        --------
        psi_alpha, psi_beta, psi_mag : float
            Flux linkages and magnitude
        """
        # Integrate: psi = integral(v - Rs*i)dt
        # Simplified estimation (need proper integration in practice)
        psi_alpha = (v_alpha - Rs * i_alpha) * dt
        psi_beta = (v_beta - Rs * i_beta) * dt

        psi_mag = np.sqrt(psi_alpha**2 + psi_beta**2)

        return psi_alpha, psi_beta, psi_mag

    def estimate_torque(self, psi_alpha, psi_beta, i_alpha, i_beta, poles):
        """
        Estimate electromagnetic torque

        Parameters:
        -----------
        psi_alpha, psi_beta : float
            Flux linkages
        i_alpha, i_beta : float
            Currents
        poles : int
            Number of poles

        Returns:
        --------
        Te : float
            Electromagnetic torque
        """
        Te = (3/2) * (poles/2) * (psi_alpha * i_beta - psi_beta * i_alpha)
        return Te

    def determine_sector(self, psi_alpha, psi_beta):
        """
        Determine flux sector (1-6)

        Parameters:
        -----------
        psi_alpha, psi_beta : float
            Flux linkages

        Returns:
        --------
        sector : int (1-6)
        """
        angle = np.arctan2(psi_beta, psi_alpha)
        if angle < 0:
            angle += 2 * np.pi

        sector = int(angle / (np.pi / 3)) + 1
        sector = np.clip(sector, 1, 6)

        return sector

    def compute(self, torque_ref, flux_mag, torque_actual, psi_alpha, psi_beta):
        """
        Compute DTC control signals

        Parameters:
        -----------
        torque_ref : float
            Reference torque
        flux_mag : float
            Actual flux magnitude
        torque_actual : float
            Actual torque
        psi_alpha, psi_beta : float
            Flux linkages in alpha-beta frame

        Returns:
        --------
        v_alpha, v_beta : float
            Selected voltage vector
        """
        # Torque error
        torque_error = torque_ref - torque_actual

        # Flux error
        flux_error = self.flux_ref - flux_mag

        # Hysteresis comparators
        if torque_error > self.torque_hyst:
            self.torque_flag = 1
        elif torque_error < -self.torque_hyst:
            self.torque_flag = -1
        else:
            self.torque_flag = 0

        if flux_error > self.flux_hyst:
            self.flux_flag = 1
        elif flux_error < -self.flux_hyst:
            self.flux_flag = -1
        else:
            self.flux_flag = 0

        # Determine sector
        self.sector = self.determine_sector(psi_alpha, psi_beta)

        # Select voltage vector from switching table
        vector_index = self.switching_table[
            self.flux_flag + 1,
            self.torque_flag + 1,
            self.sector - 1
        ]

        # Get voltage vector
        v_alpha, v_beta = self.voltage_vectors[vector_index]

        return v_alpha, v_beta

    def get_status(self):
        """Get controller status"""
        return {
            'sector': self.sector,
            'torque_flag': self.torque_flag,
            'flux_flag': self.flux_flag,
            'flux_ref': self.flux_ref
        }

    def set_flux_reference(self, flux_ref):
        """Set flux reference"""
        self.flux_ref = flux_ref
