"""
V/f (Voltage/Frequency) Control
Scalar control for induction motors
"""

import numpy as np
from .pid_controller import PIDController


class VfController:
    """
    Voltage/Frequency (V/f) Control

    Implements scalar control with:
    - Constant V/f ratio
    - Frequency ramping
    - Boost voltage for low frequencies
    - Optional slip compensation
    """

    def __init__(self, rated_voltage=380, rated_freq=50, min_freq=5,
                 max_freq=60, boost_voltage=10, ramp_rate=10):
        """
        Initialize V/f controller

        Parameters:
        -----------
        rated_voltage : float
            Rated RMS voltage (V)
        rated_freq : float
            Rated frequency (Hz)
        min_freq : float
            Minimum frequency (Hz)
        max_freq : float
            Maximum frequency (Hz)
        boost_voltage : float
            Low frequency voltage boost (V)
        ramp_rate : float
            Frequency ramp rate (Hz/s)
        """
        self.rated_voltage = rated_voltage
        self.rated_freq = rated_freq
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.boost_voltage = boost_voltage
        self.ramp_rate = ramp_rate

        # V/f ratio
        self.vf_ratio = rated_voltage / rated_freq

        # Current frequency
        self.freq = 0.0

        # Target frequency
        self.freq_target = 0.0

        # Slip compensation
        self.slip_compensation = False
        self.slip_gain = 0.1

        # Speed controller for closed-loop operation
        self.speed_controller = PIDController(
            Kp=0.1, Ki=1.0, Kd=0.001,
            output_limits=(min_freq, max_freq)
        )

    def reset(self):
        """Reset controller"""
        self.freq = 0.0
        self.freq_target = 0.0
        self.speed_controller.reset()

    def set_frequency_reference(self, freq_ref):
        """
        Set target frequency

        Parameters:
        -----------
        freq_ref : float
            Target frequency (Hz)
        """
        self.freq_target = np.clip(freq_ref, self.min_freq, self.max_freq)

    def set_speed_reference(self, speed_rpm, poles):
        """
        Set target speed (converts to frequency)

        Parameters:
        -----------
        speed_rpm : float
            Target speed (RPM)
        poles : int
            Number of motor poles
        """
        # Convert RPM to frequency
        freq_ref = speed_rpm * poles / 120.0
        self.set_frequency_reference(freq_ref)

    def enable_slip_compensation(self, enable=True, gain=0.1):
        """
        Enable/disable slip compensation

        Parameters:
        -----------
        enable : bool
            Enable slip compensation
        gain : float
            Slip compensation gain
        """
        self.slip_compensation = enable
        self.slip_gain = gain

    def ramp_frequency(self, dt):
        """
        Apply frequency ramping

        Parameters:
        -----------
        dt : float
            Time step (seconds)
        """
        freq_error = self.freq_target - self.freq
        max_change = self.ramp_rate * dt

        if abs(freq_error) < max_change:
            self.freq = self.freq_target
        elif freq_error > 0:
            self.freq += max_change
        else:
            self.freq -= max_change

    def calculate_voltage(self, freq=None):
        """
        Calculate voltage based on V/f ratio

        Parameters:
        -----------
        freq : float, optional
            Frequency (uses self.freq if not provided)

        Returns:
        --------
        voltage : float
            Output voltage magnitude
        """
        if freq is None:
            freq = self.freq

        # Base voltage from V/f ratio
        voltage = self.vf_ratio * freq

        # Add boost voltage at low frequencies
        if freq < self.rated_freq * 0.3:
            boost_factor = 1.0 - (freq / (self.rated_freq * 0.3))
            voltage += self.boost_voltage * boost_factor

        # Limit voltage
        voltage = np.clip(voltage, 0, self.rated_voltage * 1.1)

        return voltage

    def compute_open_loop(self, dt):
        """
        Compute V/f control in open-loop mode

        Parameters:
        -----------
        dt : float
            Time step

        Returns:
        --------
        freq : float
            Output frequency (Hz)
        voltage : float
            Output voltage magnitude (V)
        omega_e : float
            Electrical angular frequency (rad/s)
        """
        # Apply frequency ramping
        self.ramp_frequency(dt)

        # Calculate voltage
        voltage = self.calculate_voltage()

        # Calculate angular frequency
        omega_e = 2 * np.pi * self.freq

        return self.freq, voltage, omega_e

    def compute_closed_loop(self, speed_ref, speed_actual, poles, dt):
        """
        Compute V/f control in closed-loop mode (with speed feedback)

        Parameters:
        -----------
        speed_ref : float
            Reference speed (RPM)
        speed_actual : float
            Actual speed (rad/s)
        poles : int
            Number of poles
        dt : float
            Time step

        Returns:
        --------
        freq : float
            Output frequency (Hz)
        voltage : float
            Output voltage magnitude (V)
        omega_e : float
            Electrical angular frequency (rad/s)
        """
        # Convert speed to RPM
        speed_actual_rpm = speed_actual * 60 / (2 * np.pi)

        # Speed control loop -> frequency reference
        freq_ref = self.speed_controller.compute(speed_ref, speed_actual_rpm, dt)
        self.set_frequency_reference(freq_ref)

        # Apply frequency ramping
        self.ramp_frequency(dt)

        # Slip compensation
        if self.slip_compensation:
            # Estimate slip
            n_sync = 120 * self.freq / poles
            slip_rpm = n_sync - speed_actual_rpm
            slip_compensation_freq = slip_rpm * poles / 120.0 * self.slip_gain
            compensated_freq = self.freq + slip_compensation_freq
        else:
            compensated_freq = self.freq

        # Calculate voltage
        voltage = self.calculate_voltage(compensated_freq)

        # Calculate angular frequency
        omega_e = 2 * np.pi * compensated_freq

        return compensated_freq, voltage, omega_e

    def get_vf_curve(self, freq_points=100):
        """
        Get V/f characteristic curve

        Parameters:
        -----------
        freq_points : int
            Number of points in curve

        Returns:
        --------
        freqs : array
            Frequency points
        voltages : array
            Corresponding voltages
        """
        freqs = np.linspace(self.min_freq, self.max_freq, freq_points)
        voltages = np.array([self.calculate_voltage(f) for f in freqs])

        return freqs, voltages

    def get_status(self):
        """Get controller status"""
        return {
            'freq': self.freq,
            'freq_target': self.freq_target,
            'voltage': self.calculate_voltage(),
            'vf_ratio': self.vf_ratio,
            'slip_compensation': self.slip_compensation
        }
