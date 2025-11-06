"""
Induction Motor Model
Implements three-phase induction motor dynamics in dq reference frame
"""

import numpy as np


class InductionMotor:
    """
    Three-Phase Induction Motor Model (Squirrel Cage)

    Uses dq-axis representation in synchronous reference frame
    State variables: [isd, isq, ird, irq, omega, theta]
    """

    def __init__(self, Rs=1.0, Rr=0.8, Ls=0.1, Lr=0.1, Lm=0.09,
                 J=0.05, B=0.001, poles=4, rated_voltage=380, rated_freq=50):
        """
        Initialize induction motor parameters

        Parameters:
        -----------
        Rs : float
            Stator resistance (Ohm)
        Rr : float
            Rotor resistance (Ohm)
        Ls : float
            Stator inductance (H)
        Lr : float
            Rotor inductance (H)
        Lm : float
            Magnetizing inductance (H)
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
        self.Rr = Rr
        self.Ls = Ls
        self.Lr = Lr
        self.Lm = Lm
        self.J = J
        self.B = B
        self.poles = poles
        self.rated_voltage = rated_voltage
        self.rated_freq = rated_freq

        # Derived parameters
        self.Lls = Ls - Lm  # Stator leakage inductance
        self.Llr = Lr - Lm  # Rotor leakage inductance
        self.omega_sync = 2 * np.pi * rated_freq  # Synchronous speed

        # State variables (dq reference frame)
        self.isd = 0.0  # d-axis stator current
        self.isq = 0.0  # q-axis stator current
        self.ird = 0.0  # d-axis rotor current
        self.irq = 0.0  # q-axis rotor current
        self.omega = 0.0  # Rotor angular velocity (rad/s)
        self.theta = 0.0  # Rotor angular position (rad)
        self.theta_e = 0.0  # Electrical angle

        # External inputs
        self.Vsd = 0.0  # d-axis stator voltage
        self.Vsq = 0.0  # q-axis stator voltage
        self.TL = 0.0   # Load torque
        self.omega_e = self.omega_sync  # Electrical frequency

    def set_state(self, isd, isq, ird, irq, omega, theta):
        """Set motor state variables"""
        self.isd = isd
        self.isq = isq
        self.ird = ird
        self.irq = irq
        self.omega = omega
        self.theta = theta

    def get_state(self):
        """Get current state variables"""
        return np.array([self.isd, self.isq, self.ird, self.irq, self.omega, self.theta])

    def set_inputs(self, Vsd, Vsq, TL=None, omega_e=None):
        """Set motor inputs"""
        self.Vsd = Vsd
        self.Vsq = Vsq
        if TL is not None:
            self.TL = TL
        if omega_e is not None:
            self.omega_e = omega_e

    def dynamics(self, state, Vsd, Vsq, TL, omega_e):
        """
        Compute state derivatives in dq reference frame

        Returns: [disd/dt, disq/dt, dird/dt, dirq/dt, domega/dt, dtheta/dt]
        """
        isd, isq, ird, irq, omega, theta = state

        # Electrical rotor speed
        omega_r = omega * self.poles / 2

        # Slip frequency
        omega_slip = omega_e - omega_r

        # Calculate flux linkages
        psi_sd = self.Ls * isd + self.Lm * ird
        psi_sq = self.Ls * isq + self.Lm * irq
        psi_rd = self.Lr * ird + self.Lm * isd
        psi_rq = self.Lr * irq + self.Lm * isq

        # Stator current derivatives
        disd_dt = (Vsd - self.Rs * isd + omega_e * psi_sq) / self.Ls
        disq_dt = (Vsq - self.Rs * isq - omega_e * psi_sd) / self.Ls

        # Rotor current derivatives
        dird_dt = (-self.Rr * ird + omega_slip * psi_rq) / self.Lr
        dirq_dt = (-self.Rr * irq - omega_slip * psi_rd) / self.Lr

        # Electromagnetic torque
        Te = (3/2) * (self.poles/2) * self.Lm * (isq * ird - isd * irq)

        # Mechanical equation
        domega_dt = (Te - TL - self.B * omega) / self.J

        # Angular position
        dtheta_dt = omega

        return np.array([disd_dt, disq_dt, dird_dt, dirq_dt, domega_dt, dtheta_dt])

    def step(self, dt):
        """
        Perform one simulation step using RK4 integration

        Parameters:
        -----------
        dt : float
            Time step (seconds)
        """
        state = self.get_state()
        Vsd, Vsq, TL, omega_e = self.Vsd, self.Vsq, self.TL, self.omega_e

        # RK4 integration
        k1 = self.dynamics(state, Vsd, Vsq, TL, omega_e)
        k2 = self.dynamics(state + 0.5*dt*k1, Vsd, Vsq, TL, omega_e)
        k3 = self.dynamics(state + 0.5*dt*k2, Vsd, Vsq, TL, omega_e)
        k4 = self.dynamics(state + dt*k3, Vsd, Vsq, TL, omega_e)

        new_state = state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)

        self.isd, self.isq, self.ird, self.irq, self.omega, self.theta = new_state

        # Update electrical angle
        self.theta_e += omega_e * dt

        return self.get_measurements()

    def get_measurements(self):
        """
        Get motor measurements

        Returns:
        --------
        dict with measured values
        """
        # Electromagnetic torque
        Te = (3/2) * (self.poles/2) * self.Lm * (self.isq * self.ird - self.isd * self.irq)

        # Speed in RPM
        speed_rpm = self.omega * 60 / (2 * np.pi)

        # Synchronous speed
        n_sync = self.omega_e * 60 / (2 * np.pi)

        # Slip
        slip = (n_sync - speed_rpm) / n_sync if n_sync > 0 else 0

        # Stator current magnitude
        Is = np.sqrt(self.isd**2 + self.isq**2)

        # Rotor current magnitude
        Ir = np.sqrt(self.ird**2 + self.irq**2)

        # Flux linkages
        psi_sd = self.Ls * self.isd + self.Lm * self.ird
        psi_sq = self.Ls * self.isq + self.Lm * self.irq
        psi_s = np.sqrt(psi_sd**2 + psi_sq**2)

        # Power calculations
        Ps = 1.5 * (self.Vsd * self.isd + self.Vsq * self.isq)  # Stator power
        Pout = Te * self.omega  # Output power

        # Power factor (approximate)
        Vs = np.sqrt(self.Vsd**2 + self.Vsq**2)
        if Vs * Is > 0.1:
            pf = Ps / (1.5 * Vs * Is)
            pf = np.clip(pf, -1, 1)
        else:
            pf = 0

        # Efficiency
        efficiency = (Pout / Ps * 100) if Ps > 1 else 0

        return {
            'isd': self.isd,
            'isq': self.isq,
            'Is': Is,
            'ird': self.ird,
            'irq': self.irq,
            'Ir': Ir,
            'omega': self.omega,
            'speed_rpm': speed_rpm,
            'theta': self.theta,
            'Te': Te,
            'slip': slip,
            'psi_s': psi_s,
            'Ps': Ps,
            'Pout': Pout,
            'pf': pf,
            'efficiency': efficiency,
            'n_sync': n_sync
        }
