"""Graph construction and adjacency utilities.

Graphs are simple, undirected, and carry NO self-loops; the self-weighting
in the local mean action is handled by the 1/(d_i + 1) prefactor in the
dynamics/observables, following Damian's notes.
"""

import networkx as nx
import numpy as np

__all__ = [
    "adjacency",
    "as_graph",
    "erg_connected",
    "complete",
    "path",
    "cycle",
    "star",
    "paw",
]


def adjacency(G):
    """Symmetric adjacency matrix (float, zero diagonal) from a networkx
    graph or an array-like."""
    if isinstance(G, nx.Graph):
        A = nx.to_numpy_array(G, dtype=float)
    else:
        A = np.asarray(G, dtype=float).copy()
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("adjacency must be square")
    if not np.allclose(A, A.T):
        raise ValueError("adjacency must be symmetric (undirected graph)")
    np.fill_diagonal(A, 0.0)
    return A


def as_graph(G):
    """Return a networkx Graph from a graph or adjacency array."""
    if isinstance(G, nx.Graph):
        return G
    return nx.from_numpy_array(adjacency(G))


def erg_connected(n, p_edge, rng=None, max_tries=100_000):
    """Erdos-Renyi-Gilbert G(n, p), resampled until connected -- the
    topology generator used in Conrad & Tabor (2024)."""
    rng = np.random.default_rng(rng)
    for _ in range(max_tries):
        G = nx.erdos_renyi_graph(n, p_edge, seed=int(rng.integers(2**32)))
        if nx.is_connected(G):
            return G
    raise RuntimeError(
        f"no connected G({n}, {p_edge}) found in {max_tries} tries"
    )


def complete(n):
    """K_n."""
    return nx.complete_graph(n)


def path(n):
    """Path on n nodes: 0-1-...-(n-1)."""
    return nx.path_graph(n)


def cycle(n):
    """Cycle on n nodes."""
    return nx.cycle_graph(n)


def star(n):
    """Star with center 0 and n-1 leaves (n nodes total)."""
    return nx.star_graph(n - 1)


def paw():
    """The paw: triangle {0, 1, 2} with pendant 3 hanging off hub 2.

    Nodes 0, 1 are the free vertices, 2 the hub, 3 the pendant --
    the smallest graph admitting fraught states (see notes.tex).
    """
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3)])
    return G
