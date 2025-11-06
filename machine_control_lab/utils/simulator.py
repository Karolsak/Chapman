"""
Simulation Engine
Manages simulation execution and data logging
"""

import numpy as np
from collections import deque


class Simulator:
    """
    Simulation Engine

    Manages:
    - Real-time simulation execution
    - Data logging and history
    - Time management
    - Performance monitoring
    """

    def __init__(self, dt=0.001, max_history=5000):
        """
        Initialize simulator

        Parameters:
        -----------
        dt : float
            Simulation time step (seconds)
        max_history : int
            Maximum number of data points to keep
        """
        self.dt = dt
        self.max_history = max_history

        # Simulation time
        self.time = 0.0

        # Data history (using deque for efficient append/pop)
        self.history = {
            'time': deque(maxlen=max_history),
            'speed': deque(maxlen=max_history),
            'torque': deque(maxlen=max_history),
            'current': deque(maxlen=max_history),
            'voltage': deque(maxlen=max_history),
            'power': deque(maxlen=max_history),
            'efficiency': deque(maxlen=max_history),
            'pf': deque(maxlen=max_history),
            'speed_ref': deque(maxlen=max_history),
            'torque_ref': deque(maxlen=max_history),
        }

        # Additional data for specific control modes
        self.aux_data = {}

        # Running state
        self.running = False
        self.paused = False

    def reset(self):
        """Reset simulation"""
        self.time = 0.0
        for key in self.history:
            self.history[key].clear()
        self.aux_data.clear()
        self.running = False
        self.paused = False

    def start(self):
        """Start simulation"""
        self.running = True
        self.paused = False

    def stop(self):
        """Stop simulation"""
        self.running = False
        self.paused = False

    def pause(self):
        """Pause simulation"""
        self.paused = True

    def resume(self):
        """Resume simulation"""
        self.paused = False

    def step(self, measurements, references=None):
        """
        Execute one simulation step and log data

        Parameters:
        -----------
        measurements : dict
            Current measurements from motor
        references : dict, optional
            Reference values (setpoints)

        Returns:
        --------
        bool : True if step was executed, False if paused
        """
        if self.paused:
            return False

        # Update time
        self.time += self.dt

        # Log data
        self.history['time'].append(self.time)

        # Motor measurements
        if 'speed_rpm' in measurements:
            self.history['speed'].append(measurements['speed_rpm'])
        elif 'omega' in measurements:
            speed_rpm = measurements['omega'] * 60 / (2 * np.pi)
            self.history['speed'].append(speed_rpm)

        if 'Te' in measurements:
            self.history['torque'].append(measurements['Te'])

        # Current
        if 'Is' in measurements:
            self.history['current'].append(measurements['Is'])
        elif 'ia' in measurements:
            self.history['current'].append(abs(measurements['ia']))
        elif 'isd' in measurements and 'isq' in measurements:
            Is = np.sqrt(measurements['isd']**2 + measurements['isq']**2)
            self.history['current'].append(Is)
        elif 'id' in measurements and 'iq' in measurements:
            Is = np.sqrt(measurements['id']**2 + measurements['iq']**2)
            self.history['current'].append(Is)

        # Voltage
        if 'Vsd' in measurements and 'Vsq' in measurements:
            Vs = np.sqrt(measurements.get('Vsd', 0)**2 + measurements.get('Vsq', 0)**2)
            self.history['voltage'].append(Vs)
        elif 'Vd' in measurements and 'Vq' in measurements:
            Vs = np.sqrt(measurements.get('Vd', 0)**2 + measurements.get('Vq', 0)**2)
            self.history['voltage'].append(Vs)
        elif 'Va' in measurements:
            self.history['voltage'].append(abs(measurements['Va']))

        # Power
        if 'Pout' in measurements:
            self.history['power'].append(measurements['Pout'])
        elif 'Ps' in measurements:
            self.history['power'].append(measurements['Ps'])
        else:
            self.history['power'].append(0)

        # Efficiency
        if 'efficiency' in measurements:
            self.history['efficiency'].append(measurements['efficiency'])
        else:
            self.history['efficiency'].append(0)

        # Power factor
        if 'pf' in measurements:
            self.history['pf'].append(measurements['pf'])
        else:
            self.history['pf'].append(0)

        # References
        if references:
            if 'speed_ref' in references:
                self.history['speed_ref'].append(references['speed_ref'])
            else:
                self.history['speed_ref'].append(0)

            if 'torque_ref' in references:
                self.history['torque_ref'].append(references['torque_ref'])
            else:
                self.history['torque_ref'].append(0)
        else:
            self.history['speed_ref'].append(0)
            self.history['torque_ref'].append(0)

        return True

    def get_history(self, variables=None, num_points=None):
        """
        Get simulation history

        Parameters:
        -----------
        variables : list, optional
            List of variable names to retrieve (None = all)
        num_points : int, optional
            Number of recent points to retrieve (None = all)

        Returns:
        --------
        dict : History data
        """
        if variables is None:
            variables = list(self.history.keys())

        result = {}
        for var in variables:
            if var in self.history:
                data = list(self.history[var])
                if num_points is not None:
                    data = data[-num_points:]
                result[var] = np.array(data)
            elif var in self.aux_data:
                data = list(self.aux_data[var])
                if num_points is not None:
                    data = data[-num_points:]
                result[var] = np.array(data)

        return result

    def add_custom_data(self, name, value):
        """
        Add custom data to auxiliary storage

        Parameters:
        -----------
        name : str
            Variable name
        value : float
            Value to store
        """
        if name not in self.aux_data:
            self.aux_data[name] = deque(maxlen=self.max_history)

        self.aux_data[name].append(value)

    def get_current_values(self):
        """
        Get most recent values

        Returns:
        --------
        dict : Current values
        """
        current = {}
        for key, data in self.history.items():
            if len(data) > 0:
                current[key] = data[-1]
            else:
                current[key] = 0

        return current

    def set_dt(self, dt):
        """Set simulation time step"""
        self.dt = dt

    def get_statistics(self):
        """
        Calculate statistics on recorded data

        Returns:
        --------
        dict : Statistics (mean, std, min, max)
        """
        stats = {}

        for key, data in self.history.items():
            if key == 'time' or len(data) == 0:
                continue

            data_array = np.array(data)
            stats[key] = {
                'mean': np.mean(data_array),
                'std': np.std(data_array),
                'min': np.min(data_array),
                'max': np.max(data_array)
            }

        return stats
