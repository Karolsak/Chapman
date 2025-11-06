"""
Synchronous Motor Model
Implements permanent magnet synchronous motor (PMSM) dynamics in dq reference frame
"""

import numpy as np


class SynchronousMotor:
    """
    Permanent Magnet Synchronous Motor (PMSM) Model

    Uses dq-axis representation in rotor reference frame
    State variables: [id, iq, omega, theta]
    """

    def __init__(self, Rs=0.5, Ld=0.005, Lq=0.005,
                 flux_pm=0.1, J=0.01, B=0.001, poles=4,
                 rated_voltage=300, rated_freq=50):
        """
        Initialize PMSM parameters

        Parameters:
        -----------
        Rs : float
            Stator resistance (Ohm)
        Ld : float
            d-axis inductance (H)
        Lq : float
            q-axis inductance (H)
        flux_pm : float
            Permanent magnet flux linkage (Wb)
        J : float
            Moment of inertia (kg.m^2)
        B : float
            Friction coefficient (N.m.s/rad)
        poles : int
            Number of poles
        rated_voltage : float
            Rated line voltage (V)
        rated_freq : float
            Rated frequency (Hz)
        """
        self.Rs = Rs
        self.Ld = Ld
        self.Lq = Lq
        self.flux_pm = flux_pm
        self.J = J
        self.B = B
        self.poles = poles
        self.rated_voltage = rated_voltage
        self.rated_freq = rated_freq

        # Derived parameters
        self.omega_rated = 2 * np.pi * rated_freq * 2 / poles  # Rated mechanical speed

        # State variables (dq reference frame, rotor-oriented)
        self.id = 0.0    # d-axis current
        self.iq = 0.0    # q-axis current
        self.omega = 0.0  # Rotor angular velocity (rad/s)
        self.theta = 0.0  # Rotor angular position (rad)
        self.theta_e = 0.0  # Electrical angle

        # External inputs
        self.Vd = 0.0  # d-axis voltage
        self.Vq = 0.0  # q-axis voltage
        self.TL = 0.0  # Load torque

    def set_state(self, id, iq, omega, theta):
        """Set motor state variables"""
        self.id = id
        self.iq = iq
        self.omega = omega
        self.theta = theta
        self.theta_e = theta * self.poles / 2

    def get_state(self):
        """Get current state variables"""
        return np.array([self.id, self.iq, self.omega, self.theta])

    def set_inputs(self, Vd, Vq, TL=None):
        """Set motor inputs"""
        self.Vd = Vd
        self.Vq = Vq
        if TL is not None:
            self.TL = TL

    def dynamics(self, state, Vd, Vq, TL):
        """
        Compute state derivatives in dq reference frame

        Returns: [did/dt, diq/dt, domega/dt, dtheta/dt]
        """
        id, iq, omega, theta = state

        # Electrical angular velocity
        omega_e = omega * self.poles / 2

        # Current derivatives (voltage equations)
        did_dt = (Vd - self.Rs * id + omega_e * self.Lq * iq) / self.Ld
        diq_dt = (Vq - self.Rs * iq - omega_e * (self.Ld * id + self.flux_pm)) / self.Lq

        # Electromagnetic torque
        Te = (3/2) * (self.poles/2) * (self.flux_pm * iq + (self.Ld - self.Lq) * id * iq)

        # Mechanical equation
        domega_dt = (Te - TL - self.B * omega) / self.J

        # Angular position
        dtheta_dt = omega

        return np.array([did_dt, diq_dt, domega_dt, dtheta_dt])

    def step(self, dt):
        """
        Perform one simulation step using RK4 integration

        Parameters:
        -----------
        dt : float
            Time step (seconds)
        """
        state = self.get_state()
        Vd, Vq, TL = self.Vd, self.Vq, self.TL

        # RK4 integration
        k1 = self.dynamics(state, Vd, Vq, TL)
        k2 = self.dynamics(state + 0.5*dt*k1, Vd, Vq, TL)
        k3 = self.dynamics(state + 0.5*dt*k2, Vd, Vq, TL)
        k4 = self.dynamics(state + dt*k3, Vd, Vq, TL)

        new_state = state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)

        self.id, self.iq, self.omega, self.theta = new_state

        # Update electrical angle
        self.theta_e = self.theta * self.poles / 2

        return self.get_measurements()

    def get_measurements(self):
        """
        Get motor measurements

        Returns:
        --------
        dict with measured values
        """
        # Electromagnetic torque
        Te = (3/2) * (self.poles/2) * (self.flux_pm * self.iq + (self.Ld - self.Lq) * self.id * self.iq)

        # Speed in RPM
        speed_rpm = self.omega * 60 / (2 * np.pi)

        # Current magnitude
        Is = np.sqrt(self.id**2 + self.iq**2)

        # Voltage magnitude
        Vs = np.sqrt(self.Vd**2 + self.Vq**2)

        # Flux linkages
        psi_d = self.Ld * self.id + self.flux_pm
        psi_q = self.Lq * self.iq
        psi_s = np.sqrt(psi_d**2 + psi_q**2)

        # Power calculations
        Ps = 1.5 * (self.Vd * self.id + self.Vq * self.iq)  # Input power
        Pout = Te * self.omega  # Output power

        # Power factor
        if Vs * Is > 0.1:
            pf = Ps / (1.5 * Vs * Is)
            pf = np.clip(pf, -1, 1)
        else:
            pf = 0

        # Efficiency
        efficiency = (Pout / Ps * 100) if Ps > 1 else 0

        # Electrical frequency
        freq = self.omega * self.poles / (4 * np.pi)

        return {
            'id': self.id,
            'iq': self.iq,
            'Is': Is,
            'omega': self.omega,
            'speed_rpm': speed_rpm,
            'theta': self.theta,
            'theta_e': self.theta_e,
            'Te': Te,
            'psi_d': psi_d,
            'psi_q': psi_q,
            'psi_s': psi_s,
            'Ps': Ps,
            'Pout': Pout,
            'pf': pf,
            'efficiency': efficiency,
            'freq': freq
        }
