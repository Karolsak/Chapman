"""
DC Motor Model
Implements separately excited DC motor dynamics
"""

import numpy as np


class DCMotor:
    """
    Separately Excited DC Motor Model

    State variables: [ia, omega, theta]
    - ia: armature current (A)
    - omega: angular velocity (rad/s)
    - theta: angular position (rad)
    """

    def __init__(self, Ra=0.5, La=0.01, Rf=50.0, Lf=10.0,
                 J=0.02, B=0.001, Km=0.5, poles=4):
        """
        Initialize DC motor parameters

        Parameters:
        -----------
        Ra : float
            Armature resistance (Ohm)
        La : float
            Armature inductance (H)
        Rf : float
            Field resistance (Ohm)
        Lf : float
            Field inductance (H)
        J : float
            Moment of inertia (kg.m^2)
        B : float
            Friction coefficient (N.m.s/rad)
        Km : float
            Motor constant (V.s/rad or N.m/A)
        poles : int
            Number of poles
        """
        self.Ra = Ra
        self.La = La
        self.Rf = Rf
        self.Lf = Lf
        self.J = J
        self.B = B
        self.Km = Km
        self.poles = poles

        # State variables
        self.ia = 0.0      # Armature current
        self.if_field = 0.0  # Field current
        self.omega = 0.0   # Angular velocity (rad/s)
        self.theta = 0.0   # Angular position (rad)

        # External inputs
        self.Va = 0.0      # Armature voltage
        self.Vf = 0.0      # Field voltage
        self.TL = 0.0      # Load torque

    def set_state(self, ia, omega, theta, if_field=None):
        """Set motor state variables"""
        self.ia = ia
        self.omega = omega
        self.theta = theta
        if if_field is not None:
            self.if_field = if_field

    def get_state(self):
        """Get current state variables"""
        return np.array([self.ia, self.omega, self.theta, self.if_field])

    def set_inputs(self, Va, Vf=None, TL=None):
        """Set motor inputs"""
        self.Va = Va
        if Vf is not None:
            self.Vf = Vf
        if TL is not None:
            self.TL = TL

    def dynamics(self, state, Va, Vf, TL):
        """
        Compute state derivatives

        Returns: [dia/dt, domega/dt, dtheta/dt, dif/dt]
        """
        ia, omega, theta, if_field = state

        # Back EMF
        Ea = self.Km * if_field * omega

        # Armature current derivative
        dia_dt = (Va - Ea - self.Ra * ia) / self.La

        # Field current derivative
        dif_dt = (Vf - self.Rf * if_field) / self.Lf

        # Electromagnetic torque
        Te = self.Km * if_field * ia

        # Angular acceleration
        domega_dt = (Te - self.TL - self.B * omega) / self.J

        # Angular velocity (dtheta/dt = omega)
        dtheta_dt = omega

        return np.array([dia_dt, domega_dt, dtheta_dt, dif_dt])

    def step(self, dt):
        """
        Perform one simulation step using RK4 integration

        Parameters:
        -----------
        dt : float
            Time step (seconds)
        """
        state = self.get_state()
        Va, Vf, TL = self.Va, self.Vf, self.TL

        # RK4 integration
        k1 = self.dynamics(state, Va, Vf, TL)
        k2 = self.dynamics(state + 0.5*dt*k1, Va, Vf, TL)
        k3 = self.dynamics(state + 0.5*dt*k2, Va, Vf, TL)
        k4 = self.dynamics(state + dt*k3, Va, Vf, TL)

        new_state = state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)

        self.ia, self.omega, self.theta, self.if_field = new_state

        # Return current measurements
        return self.get_measurements()

    def get_measurements(self):
        """
        Get motor measurements

        Returns:
        --------
        dict with measured values
        """
        Te = self.Km * self.if_field * self.ia  # Electromagnetic torque
        Ea = self.Km * self.if_field * self.omega  # Back EMF
        speed_rpm = self.omega * 60 / (2 * np.pi)  # Speed in RPM
        Pa = self.Va * self.ia  # Armature power
        Pout = Te * self.omega  # Output power

        # Efficiency (avoid division by zero)
        efficiency = (Pout / Pa * 100) if Pa > 0.1 else 0

        return {
            'ia': self.ia,
            'if': self.if_field,
            'omega': self.omega,
            'speed_rpm': speed_rpm,
            'theta': self.theta,
            'Te': Te,
            'Ea': Ea,
            'Pa': Pa,
            'Pout': Pout,
            'efficiency': efficiency
        }
