"""The discrete APEM dynamics (update sequence) from Damian's notes.

State: actions sigma_i in [-1, 1] (continuous), opinions q_i in {-1, +1}.
On step k draw tau ~ Exp[mean T/N] (rate N/T) and j ~ Uniform{0..N-1};
every action drifts sigma_i -> clip(sigma_i + q_i * tau, -1, 1); then
player j's opinion flips, q_j -> -q_j, iff

    -u < sigma_bar_j < u   and   abs(sigma_j) > l,

where sigma_bar_j = (sigma_j + sum_k A_jk sigma_k) / (d_j + 1) is the
local mean action.  T is the only dimensionless timescale; u and l are
the agreement (flexibility) and position thresholds (a_theta and
s_theta of Conrad & Tabor 2024).

The inter-event law is pluggable: "exp" recovers the paper (exact
embedded chain); a float h gives the fixed-step variant (a *different*
model -- the robustness knob for the criticality program); a callable
rng -> tau gives anything else.
"""

from dataclasses import dataclass, field

import numpy as np

from .graph import adjacency

__all__ = ["Game", "Trajectory"]


@dataclass
class Trajectory:
    """Full event record of a run.

    Arrays are indexed so that row k of ``t``/``sigma``/``q`` is the state
    *after* event k (row 0 is the initial state); ``player[k]`` and
    ``flipped[k]`` describe event k+1's actor.  Positions are exact at
    event times; between events each sigma_i moves linearly toward q_i
    (clipped at +/-1).
    """

    t: np.ndarray          # (K+1,) event times, t[0] = 0
    sigma: np.ndarray      # (K+1, n) actions after each event
    q: np.ndarray          # (K+1, n) opinions after each event
    player: np.ndarray     # (K,) who fired
    flipped: np.ndarray    # (K,) bool, did they flip
    A: np.ndarray          # adjacency used
    params: dict           # u, l, T, step law, seed info
    absorbed: bool         # reached a flip-proof corner fixed point
    meta: dict = field(default_factory=dict)

    @property
    def n(self):
        return self.sigma.shape[1]

    @property
    def steps(self):
        return len(self.player)

    @property
    def t_end(self):
        return float(self.t[-1])

    def state(self, k):
        """(sigma, q) after event k."""
        return self.sigma[k], self.q[k]

    def final_state(self):
        return self.sigma[-1], self.q[-1]

    def flip_times(self):
        """Times of actual opinion flips."""
        return self.t[1:][self.flipped]

    def durations(self):
        """Interval lengths between consecutive events, shape (K,)."""
        return np.diff(self.t)


class Game:
    """APEM on an arbitrary graph.

    Parameters
    ----------
    G : networkx.Graph or adjacency array (no self-loops)
    u : agreement threshold (flip requires abs(sigma_bar_j) < u)
    l : position threshold (flip requires abs(sigma_j) > l)
    T : timescale; inter-event tau ~ Exp with mean T/N by default
    step_law : "exp" (default), a positive float h for fixed steps,
        or a callable rng -> tau.
    """

    def __init__(self, G, u, l, T, step_law="exp"):
        self.A = adjacency(G)
        self.n = self.A.shape[0]
        self.deg = self.A.sum(axis=1)
        if not 0.0 <= l < u <= 1.0:
            raise ValueError("need 0 <= l < u <= 1 (Delta = u - l > 0)")
        if T <= 0:
            raise ValueError("T must be positive")
        self.u, self.l, self.T = float(u), float(l), float(T)
        self.step_law = step_law

    # ------------------------------------------------------------------ #

    def _make_tau(self, rng):
        if self.step_law == "exp":
            mean = self.T / self.n
            return lambda: rng.exponential(mean)
        if callable(self.step_law):
            return lambda: float(self.step_law(rng))
        h = float(self.step_law)
        if h <= 0:
            raise ValueError("fixed step must be positive")
        return lambda: h

    def local_mean(self, sigma, j=None):
        """sigma_bar (all players, or just player j)."""
        if j is None:
            return (sigma + self.A @ sigma) / (self.deg + 1.0)
        return (sigma[j] + self.A[j] @ sigma) / (self.deg[j] + 1.0)

    def _is_absorbed(self, sigma, q):
        """Flip-proof corner fixed point: every action pinned at its
        opinion's wall and every agreement window shut (|sigma_bar| >= u).
        At corners |sigma_j| = 1 > l always, so the position condition
        is moot; consensus is the special case sigma = q = +/-1^n."""
        if not (np.all(np.abs(sigma) == 1.0) and np.all(sigma == q)):
            return False
        return bool(np.all(np.abs(self.local_mean(sigma)) >= self.u))

    # ------------------------------------------------------------------ #

    def run(
        self,
        sigma0=None,
        q0=None,
        max_steps=100_000,
        max_time=None,
        rng=None,
        stop_when_absorbed=True,
    ):
        """Run the update sequence; returns a Trajectory.

        sigma0 defaults to Uniform[-1, 1]^n, q0 to Uniform{-1, +1}^n.
        Stops at max_steps, at max_time (event time), or on absorption.
        """
        rng = np.random.default_rng(rng)

        if sigma0 is None:
            sigma = rng.uniform(-1.0, 1.0, self.n)
        else:
            sigma = np.asarray(sigma0, dtype=float).copy()
            if sigma.shape != (self.n,) or np.any(np.abs(sigma) > 1):
                raise ValueError("sigma0 must be n values in [-1, 1]")
        if q0 is None:
            q = rng.choice([-1.0, 1.0], self.n)
        else:
            q = np.asarray(q0, dtype=float).copy()
            if q.shape != (self.n,) or not np.all(np.abs(q) == 1.0):
                raise ValueError("q0 must be n values in {-1, +1}")

        draw_tau = self._make_tau(rng)

        ts = [0.0]
        sigmas = [sigma.copy()]
        qs = [q.copy()]
        players = []
        flips = []
        t = 0.0
        absorbed = self._is_absorbed(sigma, q) and stop_when_absorbed

        while not absorbed and len(players) < max_steps:
            tau = draw_tau()
            j = int(rng.integers(self.n))
            t += tau
            np.clip(sigma + q * tau, -1.0, 1.0, out=sigma)

            sbar_j = self.local_mean(sigma, j)
            do_flip = (-self.u < sbar_j < self.u) and (abs(sigma[j]) > self.l)
            if do_flip:
                q[j] = -q[j]

            ts.append(t)
            sigmas.append(sigma.copy())
            qs.append(q.copy())
            players.append(j)
            flips.append(do_flip)

            if stop_when_absorbed and self._is_absorbed(sigma, q):
                absorbed = True
            if max_time is not None and t >= max_time:
                break

        return Trajectory(
            t=np.array(ts),
            sigma=np.array(sigmas),
            q=np.array(qs),
            player=np.array(players, dtype=int),
            flipped=np.array(flips, dtype=bool),
            A=self.A,
            params={
                "u": self.u,
                "l": self.l,
                "T": self.T,
                "step_law": (
                    "exp" if self.step_law == "exp"
                    else "callable" if callable(self.step_law)
                    else float(self.step_law)
                ),
                "n": self.n,
            },
            absorbed=absorbed,
        )
