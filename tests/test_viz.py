import matplotlib
import numpy as np
import pytest

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

import pycoop as pc  # noqa: E402
from pycoop import viz  # noqa: E402


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


@pytest.fixture
def traj():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    return game.run(rng=7, max_steps=60)


def test_snapshot_returns_axes_and_layout():
    G = pc.paw()
    ax, pos = viz.snapshot(G, np.array([1.0, -1.0, 0.5, -0.5]),
                           q=np.array([1.0, -1.0, 1.0, -1.0]), colorbar=True)
    assert ax is not None
    assert set(pos) == set(G.nodes)


def test_snapshot_reuses_a_given_layout():
    G = pc.paw()
    _, pos = viz.snapshot(G, np.zeros(4))
    ax2, pos2 = viz.snapshot(G, np.zeros(4), pos=pos)
    assert pos2 is pos


def test_traces_draws_one_line_per_player(traj):
    ax = viz.traces(traj)
    assert len(ax.get_lines()) == traj.n


def test_traces_subset_of_players(traj):
    ax = viz.traces(traj, players=[0, 1], bands=False, flips=False)
    assert len(ax.get_lines()) == 2


def test_animate_produces_frames(traj):
    anim = viz.animate(traj, stride=5)
    assert list(anim.new_frame_seq()) == list(range(0, traj.sigma.shape[0], 5))
    plt.gcf().canvas.draw()


def test_scrub_requires_ipywidgets(monkeypatch, traj):
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "ipywidgets":
            raise ImportError("no ipywidgets")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(ImportError, match="ipywidgets"):
        viz.scrub(traj)
