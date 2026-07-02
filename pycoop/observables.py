"""Observables on states and trajectories.

State functions take (A, sigma) with A a zero-diagonal symmetric
adjacency; the self-weighting enters through 1/(d_i + 1).  Definitions
follow the main text of Conrad & Tabor (2024) as pinned down in
notes.tex: friends/enemies are statements about ACTIONS (sign of
sigma_j), not opinions, and fraughtness is the non-Pareto-optimal Nash
condition (crowd split, no single player can improve their own
agreement by switching sides).
"""

import numpy as np

__all__ = [
    "local_mean",
    "agreement",
    "friend_enemy_weights",
    "alignment_asymmetry",
    "is_consensus",
    "is_fraught",
    "is_obdurate",
    "classify",
    "mean_action",
    "mean_opinion",
    "classify_trajectory",
    "state_fractions",
    "alpha_estimate",
]


# ---------------------------- state functions ---------------------------- #

def local_mean(A, sigma):
    """sigma_bar_i = (sigma_i + sum_j A_ij sigma_j) / (d_i + 1)."""
    A = np.asarray(A, float)
    sigma = np.asarray(sigma, float)
    return (sigma + A @ sigma) / (A.sum(axis=1) + 1.0)


def agreement(A, sigma):
    """a_i = |sigma_bar_i| in [0, 1]."""
    return np.abs(local_mean(A, sigma))


def friend_enemy_weights(A, sigma):
    """(F, E): summed |sigma_j| over neighbors sharing / opposing
    player i's action sign.  Assumes sigma_i != 0 for all i."""
    A = np.asarray(A, float)
    sigma = np.asarray(sigma, float)
    s = np.sign(sigma)
    same = (s[:, None] == s[None, :])
    absw = np.abs(sigma)
    F = (A * same) @ absw
    E = (A * ~same) @ absw
    return F, E


def alignment_asymmetry(A, sigma):
    """y_i = F_i - E_i; y_i >= 0 means no local incentive to defect."""
    F, E = friend_enemy_weights(A, sigma)
    return F - E


def is_consensus(sigma):
    """In a consensus orthant: all actions share one sign, none zero."""
    s = np.sign(np.asarray(sigma, float))
    return bool(np.all(s > 0) or np.all(s < 0))


def is_fraught(A, sigma):
    """No zeros, non-consensus, and every y_i >= 0: split but locally
    content -- a non-Pareto-optimal Nash equilibrium."""
    sigma = np.asarray(sigma, float)
    if np.any(sigma == 0.0) or is_consensus(sigma):
        return False
    return bool(np.all(alignment_asymmetry(A, sigma) >= 0.0))


def is_obdurate(A, sigma):
    """No zeros, non-consensus, not fraught: some player could improve
    their agreement by switching sides (some y_i < 0) but is unwilling."""
    sigma = np.asarray(sigma, float)
    if np.any(sigma == 0.0) or is_consensus(sigma):
        return False
    return bool(np.any(alignment_asymmetry(A, sigma) < 0.0))


def classify(A, sigma):
    """One of 'consensus' | 'fraught' | 'obdurate' | 'indeterminate'
    (the last only when some sigma_i == 0 off consensus)."""
    sigma = np.asarray(sigma, float)
    if is_consensus(sigma):
        return "consensus"
    if np.any(sigma == 0.0):
        return "indeterminate"
    if np.all(alignment_asymmetry(A, sigma) >= 0.0):
        return "fraught"
    return "obdurate"


def mean_action(sigma):
    return float(np.mean(sigma))


def mean_opinion(q):
    return float(np.mean(q))


# -------------------------- trajectory functions -------------------------- #

def classify_trajectory(traj):
    """Per-event classification of a Trajectory; list of length K+1."""
    return [classify(traj.A, s) for s in traj.sigma]


def state_fractions(traj):
    """Time-weighted fraction of the run spent in each class, evaluated
    at event states and weighted by the following interval (the state
    can change class mid-interval only by an action crossing 0 or a
    wall, so this is exact up to those crossings).  Returns a dict."""
    labels = classify_trajectory(traj)[:-1]
    dt = traj.durations()
    total = dt.sum()
    out = {}
    if total == 0:
        return {labels[-1] if labels else classify(traj.A, traj.sigma[-1]): 1.0}
    for lab in ("consensus", "fraught", "obdurate", "indeterminate"):
        w = dt[[l == lab for l in labels]].sum()
        if w > 0:
            out[lab] = float(w / total)
    return out


def alpha_estimate(traj, l=None, u=None):
    """Time-weighted fraction of players past the position threshold,
    |sigma_i| > l, restricted to intervals where the global window is
    open, |mean(sigma)| < u.  On K_N this estimates the active-window
    slope alpha = 1 - 2l/(T+2) of notes.tex; on other graphs it is a
    heuristic global proxy."""
    l = traj.params["l"] if l is None else l
    u = traj.params["u"] if u is None else u
    dt = traj.durations()
    if dt.size == 0:
        raise ValueError("trajectory has no steps")
    sig = traj.sigma[:-1]
    open_win = np.abs(sig.mean(axis=1)) < u
    w = dt * open_win
    if w.sum() == 0:
        return np.nan
    frac = (np.abs(sig) > l).mean(axis=1)
    return float((frac * w).sum() / w.sum())
