"""
A fast python module with friendly GUI for Bayesian Multi-Arm Multi-Stage Design
"""
import sys as _sys
import os as _os

_sys.path.append(_os.path.abspath('../'))

__version__ = '1.1.0a2'
__author__ = 'Zhenning Yu'
__email__ = 'yuzhenning.bio@gmail.com'
__All__=['__init__', 'main', 'TrialSimulation', 'PosteriorProbability']

from .BATS import __init__
from .BATS import main
from .BATS import FixedTrial.TrialSimulation as TrialSimulation
from .BATS import CalPosteriorProbability.CalPosteriorProbability as PosteriorProbability
