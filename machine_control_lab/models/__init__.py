"""
Electrical Machine Models Package
Includes DC, Induction, and Synchronous motor models
"""

from .dc_motor import DCMotor
from .induction_motor import InductionMotor
from .synchronous_motor import SynchronousMotor

__all__ = ['DCMotor', 'InductionMotor', 'SynchronousMotor']
