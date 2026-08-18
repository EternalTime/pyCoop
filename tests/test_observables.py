import numpy as np
import pytest

import pycoop as pc
from pycoop import observables as obs


PAW = pc.adjacency(pc.paw())


def test_local_mean_and_agreement_agree_on_consensus():
    sigma = np.ones(4)
    assert np.allclose(obs.local_mean(PAW, sigma), 1.0)
    assert np.allclose(obs.agreement(PAW, sigma), 1.0)


def test_friend_enemy_weights_split_by_action_sign():
    A = pc.adjacency(pc.complete(3))
    sigma = np.array([1.0, 1.0, -0.5])
    F, E = obs.friend_enemy_weights(A, sigma)
    assert F == pytest.approx([1.0, 1.0, 0.0])
    assert E == pytest.approx([0.5, 0.5, 2.0])
    assert obs.alignment_asymmetry(A, sigma) == pytest.approx([0.5, 0.5, -2.0])


def test_consensus_detection():
    assert obs.is_consensus(np.ones(4))
    assert obs.is_consensus(-np.ones(4))
    assert not obs.is_consensus(np.array([1.0, -1.0, 1.0, 1.0]))
    assert not obs.is_consensus(np.array([1.0, 0.0, 1.0, 1.0]))


def test_classify_consensus():
    assert obs.classify(PAW, np.ones(4)) == "consensus"


def test_classify_fraught_on_the_paw():
    sigma = np.array([-0.6, -0.3, 0.3, 1.0])
    assert obs.is_fraught(PAW, sigma)
    assert not obs.is_obdurate(PAW, sigma)
    assert obs.classify(PAW, sigma) == "fraught"


def test_classify_obdurate():
    sigma = np.array([1.0, 1.0, -1.0, -1.0])
    assert obs.is_obdurate(PAW, sigma)
    assert not obs.is_fraught(PAW, sigma)
    assert obs.classify(PAW, sigma) == "obdurate"


def test_classify_indeterminate_on_zero_action():
    sigma = np.array([1.0, -1.0, 0.0, -1.0])
    assert obs.classify(PAW, sigma) == "indeterminate"
    assert not obs.is_fraught(PAW, sigma)
    assert not obs.is_obdurate(PAW, sigma)


def test_mean_action_and_opinion():
    assert obs.mean_action(np.array([1.0, -1.0, 0.5, 0.5])) == pytest.approx(0.25)
    assert obs.mean_opinion(np.array([1.0, 1.0, -1.0, -1.0])) == pytest.approx(0.0)


def test_state_fractions_sum_to_one():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=7, max_steps=200)
    frac = obs.state_fractions(traj)
    assert set(frac) <= {"consensus", "fraught", "obdurate", "indeterminate"}
    assert sum(frac.values()) == pytest.approx(1.0)


def test_classify_trajectory_length():
    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=3, max_steps=30)
    assert len(obs.classify_trajectory(traj)) == traj.steps + 1


def test_state_fractions_of_a_stationary_run():
    game = pc.Game(pc.complete(4), u=0.5, l=0.2, T=1.0)
    traj = game.run(sigma0=np.ones(4), q0=np.ones(4), rng=0)
    assert obs.state_fractions(traj) == {"consensus": 1.0}


def test_alpha_estimate_is_a_fraction():
    game = pc.Game(pc.complete(6), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=5, max_steps=300)
    alpha = obs.alpha_estimate(traj)
    assert np.isnan(alpha) or 0.0 <= alpha <= 1.0


def test_alpha_estimate_needs_steps():
    game = pc.Game(pc.complete(4), u=0.5, l=0.2, T=1.0)
    traj = game.run(sigma0=np.ones(4), q0=np.ones(4), rng=0)
    with pytest.raises(ValueError):
        obs.alpha_estimate(traj)
