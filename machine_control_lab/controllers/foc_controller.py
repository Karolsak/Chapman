"""
Field Oriented Control (FOC) Controller
Vector control for AC motors (Induction and PMSM)
"""

import numpy as np
from .pid_controller import PIDController


class FOCController:
    """
    Field Oriented Control (Vector Control)

    Implements FOC with:
    - Speed control loop
    - Current control loops (id, iq)
    - Park and Clarke transformations
    - Space Vector Modulation (SVM)
    """

    def __init__(self, motor_type='PMSM', poles=4, Vdc=400,
                 speed_Kp=0.5, speed_Ki=10, speed_Kd=0.001,
                 current_Kp=5, current_Ki=100, current_Kd=0):
        """
        Initialize FOC controller

        Parameters:
        -----------
        motor_type : str
            'PMSM' or 'Induction'
        poles : int
            Number of motor poles
        Vdc : float
            DC bus voltage
        speed_Kp, speed_Ki, speed_Kd : float
            Speed controller PID gains
        current_Kp, current_Ki, current_Kd : float
            Current controller PID gains
        """
        self.motor_type = motor_type
        self.poles = poles
        self.Vdc = Vdc

        # Speed controller
        self.speed_controller = PIDController(
            Kp=speed_Kp, Ki=speed_Ki, Kd=speed_Kd,
            output_limits=(-100, 100)
        )

        # Current controllers (id and iq)
        voltage_limit = Vdc / np.sqrt(3)
        self.id_controller = PIDController(
            Kp=current_Kp, Ki=current_Ki, Kd=current_Kd,
            output_limits=(-voltage_limit, voltage_limit)
        )
        self.iq_controller = PIDController(
            Kp=current_Kp, Ki=current_Ki, Kd=current_Kd,
            output_limits=(-voltage_limit, voltage_limit)
        )

        # Flux reference (for induction motor)
        self.flux_ref = 0.1  # Wb

        # Internal states
        self.theta_e = 0.0  # Electrical angle for transformations
        self.id_ref = 0.0
        self.iq_ref = 0.0

    def reset(self):
        """Reset all controllers"""
        self.speed_controller.reset()
        self.id_controller.reset()
        self.iq_controller.reset()

    def set_flux_reference(self, flux_ref):
        """Set flux reference for field weakening"""
        self.flux_ref = flux_ref

    def clarke_transform(self, ia, ib, ic):
        """
        Clarke transformation (abc -> alpha-beta)

        Parameters:
        -----------
        ia, ib, ic : float
            Three-phase currents

        Returns:
        --------
        i_alpha, i_beta : float
            Stationary reference frame currents
        """
        i_alpha = ia
        i_beta = (ia + 2*ib) / np.sqrt(3)
        return i_alpha, i_beta

    def park_transform(self, i_alpha, i_beta, theta):
        """
        Park transformation (alpha-beta -> dq)

        Parameters:
        -----------
        i_alpha, i_beta : float
            Stationary reference frame currents
        theta : float
            Electrical angle (rad)

        Returns:
        --------
        id, iq : float
            Rotating reference frame currents
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        id = i_alpha * cos_theta + i_beta * sin_theta
        iq = -i_alpha * sin_theta + i_beta * cos_theta

        return id, iq

    def inverse_park_transform(self, vd, vq, theta):
        """
        Inverse Park transformation (dq -> alpha-beta)

        Parameters:
        -----------
        vd, vq : float
            Rotating reference frame voltages
        theta : float
            Electrical angle (rad)

        Returns:
        --------
        v_alpha, v_beta : float
            Stationary reference frame voltages
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        v_alpha = vd * cos_theta - vq * sin_theta
        v_beta = vd * sin_theta + vq * cos_theta

        return v_alpha, v_beta

    def compute(self, speed_ref, speed_actual, id_actual, iq_actual, theta_e, dt):
        """
        Compute FOC control signals

        Parameters:
        -----------
        speed_ref : float
            Reference speed (rad/s)
        speed_actual : float
            Actual speed (rad/s)
        id_actual : float
            Actual d-axis current
        iq_actual : float
            Actual q-axis current
        theta_e : float
            Electrical angle (rad)
        dt : float
            Time step

        Returns:
        --------
        Vd, Vq : float
            Control voltages in dq frame
        """
        self.theta_e = theta_e

        # Speed control loop -> torque (iq) reference
        iq_ref = self.speed_controller.compute(speed_ref, speed_actual, dt)
        self.iq_ref = iq_ref

        # Flux control
        if self.motor_type == 'PMSM':
            # For PMSM, typically id_ref = 0 (maximum torque per ampere)
            id_ref = 0.0
        else:
            # For induction motor, maintain flux
            id_ref = self.flux_ref
        self.id_ref = id_ref

        # Current control loops
        Vd = self.id_controller.compute(id_ref, id_actual, dt)
        Vq = self.iq_controller.compute(iq_ref, iq_actual, dt)

        return Vd, Vq

    def compute_abc_voltages(self, Vd, Vq, theta_e):
        """
        Convert dq voltages to three-phase abc voltages

        Parameters:
        -----------
        Vd, Vq : float
            dq voltages
        theta_e : float
            Electrical angle

        Returns:
        --------
        Va, Vb, Vc : float
            Three-phase voltages
        """
        # Inverse Park transform
        v_alpha, v_beta = self.inverse_park_transform(Vd, Vq, theta_e)

        # Inverse Clarke transform
        Va = v_alpha
        Vb = -0.5 * v_alpha + (np.sqrt(3)/2) * v_beta
        Vc = -0.5 * v_alpha - (np.sqrt(3)/2) * v_beta

        return Va, Vb, Vc

    def get_references(self):
        """Get current references"""
        return {
            'id_ref': self.id_ref,
            'iq_ref': self.iq_ref
        }
