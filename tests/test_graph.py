import networkx as nx
import numpy as np
import pytest

import pycoop as pc


def test_adjacency_from_graph_is_symmetric_and_hollow():
    A = pc.adjacency(pc.paw())
    assert A.shape == (4, 4)
    assert np.allclose(A, A.T)
    assert np.all(np.diag(A) == 0.0)


def test_adjacency_strips_self_loops_from_array():
    A = pc.adjacency([[1.0, 1.0], [1.0, 1.0]])
    assert np.allclose(A, [[0.0, 1.0], [1.0, 0.0]])


def test_adjacency_rejects_non_square():
    with pytest.raises(ValueError):
        pc.adjacency(np.zeros((2, 3)))


def test_adjacency_rejects_asymmetric():
    with pytest.raises(ValueError):
        pc.adjacency([[0.0, 1.0], [0.0, 0.0]])


def test_as_graph_roundtrip():
    G = pc.as_graph(pc.adjacency(pc.cycle(5)))
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() == 5
    assert G.number_of_edges() == 5


def test_named_graphs_have_expected_shape():
    assert pc.complete(4).number_of_edges() == 6
    assert pc.path(4).number_of_edges() == 3
    assert pc.star(5).number_of_nodes() == 5
    assert sorted(d for _, d in pc.paw().degree()) == [1, 2, 2, 3]


def test_erg_connected_is_connected_and_reproducible():
    G = pc.erg_connected(10, 0.4, rng=0)
    assert nx.is_connected(G)
    assert nx.to_numpy_array(G).tolist() == \
        nx.to_numpy_array(pc.erg_connected(10, 0.4, rng=0)).tolist()


def test_erg_connected_gives_up():
    with pytest.raises(RuntimeError):
        pc.erg_connected(5, 0.0, rng=0, max_tries=3)
