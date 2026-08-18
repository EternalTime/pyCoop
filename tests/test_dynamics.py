import numpy as np
import pytest

import pycoop as pc


def test_game_rejects_bad_thresholds():
    with pytest.raises(ValueError):
        pc.Game(pc.paw(), u=0.2, l=0.5, T=1.0)
    with pytest.raises(ValueError):
        pc.Game(pc.paw(), u=0.5, l=0.2, T=0.0)


def test_local_mean_matches_definition():
    game = pc.Game(pc.path(3), u=0.5, l=0.2, T=1.0)
    sigma = np.array([1.0, 0.0, -1.0])
    expected = (sigma + game.A @ sigma) / (game.deg + 1.0)
    assert np.allclose(game.local_mean(sigma), expected)
    assert game.local_mean(sigma, 1) == pytest.approx(expected[1])


def test_run_is_reproducible_for_a_seed():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    a = game.run(rng=7)
    b = game.run(rng=7)
    assert np.array_equal(a.t, b.t)
    assert np.array_equal(a.sigma, b.sigma)
    assert np.array_equal(a.q, b.q)


def test_actions_stay_in_the_box_and_time_increases():
    game = pc.Game(pc.erg_connected(8, 0.4, rng=2), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=3, max_steps=500)
    assert np.all(np.abs(traj.sigma) <= 1.0 + 1e-12)
    assert np.all(np.diff(traj.t) > 0.0)
    assert set(np.unique(traj.q)) <= {-1.0, 1.0}


def test_trajectory_shapes_are_consistent():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=1, max_steps=50)
    k = traj.steps
    assert traj.n == 4
    assert traj.t.shape == (k + 1,)
    assert traj.sigma.shape == (k + 1, 4)
    assert traj.q.shape == (k + 1, 4)
    assert traj.player.shape == (k,)
    assert traj.flipped.shape == (k,)
    assert traj.durations().shape == (k,)
    assert traj.t_end == pytest.approx(traj.t[-1])
    assert np.array_equal(traj.state(0)[0], traj.sigma[0])
    assert np.array_equal(traj.final_state()[1], traj.q[-1])
    assert traj.flip_times().shape == (int(traj.flipped.sum()),)


def test_consensus_start_is_absorbing():
    game = pc.Game(pc.complete(4), u=0.5, l=0.2, T=1.0)
    one = np.ones(4)
    traj = game.run(sigma0=one, q0=one, rng=0)
    assert traj.absorbed
    assert traj.steps == 0


def test_fixed_step_law_gives_uniform_durations():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0, step_law=0.25)
    traj = game.run(rng=0, max_steps=20)
    assert np.allclose(traj.durations(), 0.25)


def test_callable_step_law_is_used():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0, step_law=lambda rng: 0.1)
    traj = game.run(rng=0, max_steps=10)
    assert np.allclose(traj.durations(), 0.1)


def test_nonpositive_fixed_step_rejected():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0, step_law=-1.0)
    with pytest.raises(ValueError):
        game.run(rng=0)


def test_max_time_stops_the_run():
    game = pc.Game(pc.paw(), u=0.9, l=0.1, T=1.0, step_law=0.1)
    traj = game.run(rng=0, max_time=1.0, max_steps=10_000)
    assert traj.t_end >= 1.0
    assert traj.t_end < 1.0 + 0.2


def test_bad_initial_conditions_rejected():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    with pytest.raises(ValueError):
        game.run(sigma0=np.array([2.0, 0.0, 0.0, 0.0]))
    with pytest.raises(ValueError):
        game.run(q0=np.array([0.5, 1.0, 1.0, 1.0]))
