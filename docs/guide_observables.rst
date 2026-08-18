The Observables
===============

A trajectory is just data until you ask it questions. Here are the ones
pyCoop knows how to ask.

Agreement
^^^^^^^^^

For player :math:`i`, agreement is the absolute value of the local mean
action,

.. math::

   a_i = |\bar\sigma_i| \in [0, 1],

computed by :func:`~pycoop.observables.agreement`. Note what the absolute
value hides: a crowd torn between extremes and a crowd of fence-sitters
score alike. The alignment asymmetry below repairs that.

Friends, enemies, and fraughtness
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fix a state with no player exactly at zero, and split player :math:`i`'s
neighbors by the sign of their *action*: opinions play no role here.
Friends share :math:`i`'s sign, enemies oppose it, and each camp gets a
weight,

.. math::

   F_i = \Big|\sum_{j \in \mathrm{friends}(i)} \sigma_j\Big|,
   \qquad
   E_i = \Big|\sum_{j \in \mathrm{enemies}(i)} \sigma_j\Big|,

whose difference :math:`y_i = F_i - E_i` is the *alignment asymmetry*
(:func:`~pycoop.observables.alignment_asymmetry`). A positive :math:`y_i`
says player :math:`i`'s friends outweigh their enemies, leaving no local
incentive to defect.

A state is *fraught* when three things hold at once: no player sits at
zero, the crowd is split, and every :math:`y_i \geq 0`. That is a
standoff, everyone locally content while the group has failed to
coordinate, and exactly a non-Pareto-optimal Nash equilibrium (Tabor,
Smith, and Dankowicz, 2024; Conrad and Tabor, 2024). Such states are tense
but stable: fraught, not frustrated. Fraughtness needs at least four
players. On the paw it occupies a sliver of volume :math:`1/384` of the
hypercube, on the four-path a healthier :math:`1/32`, both reproduced by
Monte Carlo with :func:`~pycoop.observables.is_fraught`.

Obdurateness
^^^^^^^^^^^^

The other way to fail. A state is *obdurate* when the crowd is split, no
player is at zero, and some player has :math:`y_i < 0`. That player could
improve their agreement by switching sides, but the dynamics won't let
them, their agreement already above threshold and their window shut. The
jam is the work of holdouts, each enjoying high agreement bought by their
neighbors' coordination while contributing nothing to it.
:func:`~pycoop.observables.is_obdurate` tests the condition, and
:func:`~pycoop.observables.classify` sorts any state into ``consensus``,
``fraught``, ``obdurate``, or ``indeterminate``.

Over a whole run
^^^^^^^^^^^^^^^^

:func:`~pycoop.observables.classify_trajectory` labels every event state,
and :func:`~pycoop.observables.state_fractions` weights those labels by
the time spent in them::

    import pycoop as pc
    from pycoop import observables as obs

    game = pc.Game(pc.erg_connected(10, 0.1, rng=0), u=0.3, l=0.5, T=0.1)
    traj = game.run(rng=1)
    print(obs.state_fractions(traj))

On the complete graph one more number is worth extracting. While the
window is open, flips only ever depolarize the crowd, and the mean opinion
decays at a rate set by the fraction of players past the position
threshold,

.. math::

   \alpha = 1 - \frac{2l}{T + 2},

a geometric occupancy fraction, which is why it holds still.
:func:`~pycoop.observables.alpha_estimate` measures it from a trajectory;
on :math:`K_{64}` the estimate matches the formula to four digits. Voila!
