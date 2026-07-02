"""pyCoop: discrete APEM dynamics on arbitrary graphs.

Implements the update sequence (the exact embedded chain of Conrad &
Tabor 2024), observables (agreement, fraughtness,
obdurateness, alpha), and visualization.
"""

from .graph import (
    adjacency, as_graph, erg_connected, complete, path, cycle, star, paw,
)
from .dynamics import Game, Trajectory
from . import observables, viz

__version__ = "0.1.0"

__all__ = [
    "adjacency", "as_graph", "erg_connected", "complete", "path",
    "cycle", "star", "paw", "Game", "Trajectory", "observables", "viz",
]
