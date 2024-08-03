"""
predicter

this module work with data extracted from aviator to try to get the pattern for the data seen
"""

from predicter.sqlite_db import PredicterDB
from predicter.probabilistic import binomial,nbinomial,geometrical
from predicter.predictions import Predictor
from predicter.data_loader import get_data