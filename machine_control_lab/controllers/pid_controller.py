"""
PID Controller
Generic PID controller with anti-windup
"""

import numpy as np


class PIDController:
    """
    PID Controller with anti-windup

    Implements discrete PID control with:
    - Proportional, Integral, and Derivative actions
    - Anti-windup protection
    - Output saturation
    """

    def __init__(self, Kp=1.0, Ki=0.1, Kd=0.01, output_limits=(-100, 100),
                 sample_time=0.001):
        """
        Initialize PID controller

        Parameters:
        -----------
        Kp : float
            Proportional gain
        Ki : float
            Integral gain
        Kd : float
            Derivative gain
        output_limits : tuple
            (min, max) output limits
        sample_time : float
            Sample time in seconds
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.output_limits = output_limits
        self.sample_time = sample_time

        # Internal states
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_measurement = None

        # Anti-windup
        self.windup_guard = abs(output_limits[1] - output_limits[0])

    def reset(self):
        """Reset controller states"""
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_measurement = None

    def set_gains(self, Kp=None, Ki=None, Kd=None):
        """Update controller gains"""
        if Kp is not None:
            self.Kp = Kp
        if Ki is not None:
            self.Ki = Ki
        if Kd is not None:
            self.Kd = Kd

    def compute(self, setpoint, measurement, dt=None):
        """
        Compute PID output

        Parameters:
        -----------
        setpoint : float
            Desired value
        measurement : float
            Current measured value
        dt : float, optional
            Time step (uses sample_time if not provided)

        Returns:
        --------
        output : float
            Control signal
        """
        if dt is None:
            dt = self.sample_time

        # Calculate error
        error = setpoint - measurement

        # Proportional term
        P = self.Kp * error

        # Integral term with anti-windup
        self.integral += error * dt
        self.integral = np.clip(self.integral,
                               -self.windup_guard / (self.Ki + 1e-10),
                               self.windup_guard / (self.Ki + 1e-10))
        I = self.Ki * self.integral

        # Derivative term (on measurement to avoid derivative kick)
        D = 0.0
        if self.prev_measurement is not None:
            derivative = -(measurement - self.prev_measurement) / dt
            D = self.Kd * derivative

        # Calculate output
        output = P + I + D

        # Apply output limits
        output = np.clip(output, self.output_limits[0], self.output_limits[1])

        # Save states
        self.prev_error = error
        self.prev_measurement = measurement

        return output

    def get_components(self, setpoint, measurement, dt=None):
        """
        Get individual P, I, D components

        Returns:
        --------
        dict with P, I, D, and output values
        """
        if dt is None:
            dt = self.sample_time

        error = setpoint - measurement

        P = self.Kp * error
        I = self.Ki * self.integral

        D = 0.0
        if self.prev_measurement is not None:
            derivative = -(measurement - self.prev_measurement) / dt
            D = self.Kd * derivative

        output = np.clip(P + I + D, self.output_limits[0], self.output_limits[1])

        return {
            'P': P,
            'I': I,
            'D': D,
            'output': output,
            'error': error
        }
