The Observables
===============

A trajectory is just data until you ask it questions. This guide covers
the questions pyCoop knows how to ask — what a state is, how content each
player is, and how the answers add up over a run.

Agreement
^^^^^^^^^

For player :math:`i`, agreement is the absolute value of the local mean
action,

.. math::

   a_i = |\bar\sigma_i| \in [0, 1],

computed by :func:`~pycoop.observables.agreement`. Note what the absolute
value hides: a crowd torn between extremes and a crowd of uniform
fence-sitters get scored as equally agreeable, which feels wrong — two
very different neighborhoods, one polarized and one lukewarm, graded
alike. That lack is what the alignment asymmetry below is built to
address.

Friends, enemies, and fraughtness
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fix a state with no player exactly at zero. Split player :math:`i`'s
neighbors by the sign of their *action* — opinions play no role here.
The friends share :math:`i`'s sign, the enemies oppose it, and each camp
gets a weight,

.. math::

   F_i = \Big|\sum_{j \in \mathrm{friends}(i)} \sigma_j\Big|,
   \qquad
   E_i = \Big|\sum_{j \in \mathrm{enemies}(i)} \sigma_j\Big|,

whose difference :math:`y_i = F_i - E_i` is the *alignment asymmetry*
(:func:`~pycoop.observables.alignment_asymmetry`). A positive :math:`y_i`
says player :math:`i`'s friends outweigh their enemies — no local
incentive to defect.

A state is *fraught* when three things hold at once: no player sits at
zero, the crowd is split, and every :math:`y_i \geq 0`. The plain reading
is a standoff — everyone is locally content, yet the group has failed to
coordinate. This is exactly a non-Pareto-optimal Nash equilibrium
(Tabor, Smith, and Dankowicz, 2024; Conrad and Tabor, 2024), and the
states are tense but stable — fraught, not frustrated. Fraughtness
needs at least four players: on the paw it occupies a sliver of volume
:math:`1/384` of the hypercube, on the four-path a healthier
:math:`1/32`, and pyCoop's :func:`~pycoop.observables.is_fraught`
reproduces both fractions by Monte Carlo.

Obdurateness
^^^^^^^^^^^^

The other way to fail. A state is *obdurate* when the crowd is split, no
player is at zero, and some player has :math:`y_i < 0` — that player
could improve their own agreement by switching sides, but the dynamics
won't let them (their agreement is already above threshold, so their
window is shut). The blame for the jam falls on individual holdouts —
each enjoying high agreement bought by their neighbors' coordination
while contributing nothing to it. :func:`~pycoop.observables.is_obdurate`
tests the condition, and :func:`~pycoop.observables.classify` sorts any
state into ``consensus``, ``fraught``, ``obdurate``, or ``indeterminate``.

Over a whole run
^^^^^^^^^^^^^^^^

:func:`~pycoop.observables.classify_trajectory` labels every event state,
and :func:`~pycoop.observables.state_fractions` weights the labels by the
time spent in them — the fraction of a run spent in each condition::

    import pycoop as pc
    from pycoop import observables as obs

    game = pc.Game(pc.erg_connected(10, 0.1, rng=0), u=0.3, l=0.5, T=0.1)
    traj = game.run(rng=1)
    print(obs.state_fractions(traj))

On the complete graph there is one more number worth extracting. While
the window is open, flips only ever depolarize the crowd, and the mean
opinion decays at a rate set by the fraction of players past the position
threshold,

.. math::

   \alpha = 1 - \frac{2l}{T + 2},

a geometric occupancy fraction — which is why it holds still.
:func:`~pycoop.observables.alpha_estimate` measures it from a trajectory;
on :math:`K_{64}` the estimate matches the formula to four digits. Voila!
