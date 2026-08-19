The Dynamics
============

A cooperation game is a piecewise-deterministic random process: ballistic
drift punctuated by randomly clocked decisions. Positions between events
are a deterministic function of the elapsed time and the headings, and the
flip rule reads the state only at decision instants, so the model
collapses losslessly to an embedded chain in which one uniformly random
player acts at each exponentially spaced event. pyCoop implements that
chain directly, with no event queue and nothing lost. The model is the
Agreement-Position Emigration model of Conrad and Tabor (2024); the
notation follows the socio-physics recasting of it, and the papers carry
the analysis.

The update sequence
^^^^^^^^^^^^^^^^^^^

Let there be :math:`N` agents on a connected graph with adjacency matrix
:math:`A_{ij}`, without self-loops. Each carries two degrees of freedom, a
continuous *action* :math:`\sigma_i \in [-1, 1]` and a binary *opinion*
:math:`q_i \in \{-1, +1\}`: a person who believes something and is doing
something about it, with no guarantee that the two agree.

On each step draw two random variables,

.. math::

   \tau \sim \mathrm{Exp}\!\left[\tfrac{N}{T}\right],
   \qquad
   j \sim \mathcal{U}_N,

the first setting how long we wait, the second who gets to act. Every
action drifts toward its opinion and is clipped at the walls,

.. math::

   \sigma_i \mapsto \min(\max(\sigma_i + q_i\,\tau,\, -1),\, 1),

and then player :math:`j` alone compares their action to their
neighborhood's. The *local mean action*

.. math::

   \bar\sigma_j = \frac{1}{d_j + 1}\Big(\sigma_j + \sum_k A_{jk}\,\sigma_k\Big)

counts the player alongside their neighbors, since an agent listens to the
crowd but weighs themselves too, which is why the prefactor is
:math:`1/(d_j+1)` rather than :math:`1/d_j`. The opinion flips,
:math:`q_j \mapsto -q_j`, iff

.. math::

   -u < \bar\sigma_j < u
   \quad\text{and}\quad
   |\sigma_j| > l.

The first condition says the neighborhood is not yet committed, the second
that this player has drifted far enough out to reconsider. :math:`T` is
the only dimensionless timescale in the problem, and the pair
:math:`(l, u)` - with :math:`\Delta = u - l > 0` - carves out the
change-of-heart regions :math:`[-u, -l] \cup [l, u]` where flips can fire.

Running a game
^^^^^^^^^^^^^^

A :class:`~pycoop.dynamics.Game` binds a graph to the three parameters::

    import pycoop as pc

    game = pc.Game(pc.erg_connected(20, 0.1, rng=0), u=0.5, l=0.2, T=0.1)
    traj = game.run(rng=1, max_steps=200_000)

``run`` takes initial conditions (``sigma0``, ``q0``; both default to
uniform draws), a step budget, a time budget (``max_time``), and a seed.
It halts early once the state is *absorbed*: every action pinned at its
opinion's wall, every agreement window shut, no flip able to fire again.
Consensus is the absorbing corner where all the signs agree; the others
hold the fraught and obdurate states.

The trajectory
^^^^^^^^^^^^^^

Everything the run did comes back in a
:class:`~pycoop.dynamics.Trajectory`: event times, the action and opinion
arrays after every event, who fired, and whether they flipped. All the
randomness sits in the iid sequence :math:`(\tau_k, j_k)`, so the
trajectory *is* the run, and every observable in the next guide is
computed from it after the fact rather than baked into the simulator.

The clock as a knob
^^^^^^^^^^^^^^^^^^^

The exponential clock is exact, but not sacred. Pass a float and every
wait becomes a fixed step :math:`h`; pass a callable and the waits follow
any law you like::

    game = pc.Game(pc.complete(64), u=0.5, l=0.2, T=2.0, step_law=0.03125)

The fixed-step variant is a genuinely different model, with positions
living on a lattice of spacing :math:`h` and step-size dispersion entering
only through the resolution near the thresholds. Whether that matters is
an empirical question, and it bears on whether the model's critical
behavior belongs to the dynamics or to the clock. If the phenomenology is
invariant to the clock law, the timescale is effectively a non-parameter,
which is worth checking rather than assuming.
