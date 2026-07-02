pyCoop
======

What does it take for a crowd to agree? Strip the question to its
skeleton: :math:`N` players on a graph, each carrying a continuous
*action* in :math:`[-1, 1]` and a binary *opinion* — a thing they are
doing and a thing they believe, with no guarantee the two line up.
Actions drift toward opinions; every so often a player compares their
action against their neighborhood's, and if they are committed to a side
yet poorly coordinated with the crowd, they change their mind. The group
wins when every action lands on the same side. From these spare rules
comes a zoo of outcomes — clean consensus, *fraught* standoffs where
every player is locally content while the group as a whole has failed,
*obdurate* jams pinned on a lone holdout — all governed by a single
timescale and a pair of thresholds.

pyCoop implements this model on arbitrary graphs. The dynamics are the
exact embedded chain of the continuous-time model — actions drift toward
opinions, opinions flip when a player is committed but poorly
coordinated — with the inter-event clock exposed as a switch, so the
exponential law and a fixed-step variant can be compared head to head.
The observables
quantify what a state *is* — its agreement, its fraughtness, its
obdurateness — and the visualization tools turn trajectories into pictures
and film.

If you're new here, start with :doc:`getting_started`, then work through
the guides in order — the dynamics first, then the observables that
classify what the dynamics produce, then the tools for looking at it all.

Guide
^^^^^

.. toctree::
   :maxdepth: 1

   getting_started
   guide_dynamics
   guide_observables
   guide_viz

Reference
^^^^^^^^^

.. toctree::
   :maxdepth: 2

   api/pycoop
   license

References
^^^^^^^^^^

Conrad, M. and Tabor, W. (2024). Intermediate flexibility in cooperation
games prevents free riding, polarization, and societal disintegration.
*Collective Intelligence*, 3(4). doi:10.1177/26339137241303908

Tabor, W., Smith, G., and Dankowicz, H. (2024). Escape from fraught
states in a coordination game. *Royal Society Open Science*,
11(2):231314.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
