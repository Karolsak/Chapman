"""
Electrical Machine Control Laboratory
A comprehensive system for modeling, simulation, and control of electrical machines

Modules:
--------
- models: Electrical machine models (DC, Induction, PMSM)
- controllers: Control algorithms (PID, FOC, DTC, V/f)
- gui: Graphical user interface
- utils: Simulation utilities
"""

__version__ = "1.0.0"
__author__ = "Machine Control Laboratory Team"

from .models import DCMotor, InductionMotor, SynchronousMotor
from .controllers import PIDController, FOCController, DTCController, VfController
from .utils import Simulator

__all__ = [
    'DCMotor',
    'InductionMotor',
    'SynchronousMotor',
    'PIDController',
    'FOCController',
    'DTCController',
    'VfController',
    'Simulator'
]
