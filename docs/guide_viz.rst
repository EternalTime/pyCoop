Visualization
=============

A cooperation game is a story — players drifting, wavering inside the
change-of-heart bands, flipping, and finally locking in — and stories are
easier to follow when you can see them. pyCoop draws states, traces, and
films, all from the same trajectory object.

Snapshots
^^^^^^^^^

:func:`~pycoop.viz.snapshot` draws a single state on the graph. Actions
color the nodes over a diverging map from :math:`-1` to :math:`+1`;
opinions set the node border — dark for :math:`+1`, light for
:math:`-1` — so a node whose fill and border disagree is a player acting
against their belief::

    import pycoop as pc
    from pycoop import viz

    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=7)

    viz.snapshot(pc.paw(), *traj.final_state(), colorbar=True)

The layout is a seeded spring layout by default; pass ``pos`` to pin your
own coordinates, and reuse the returned ``pos`` across frames so the
graph doesn't wander between figures.

Traces
^^^^^^

:func:`~pycoop.viz.traces` plots every player's action against time.
The shaded bands are the change-of-heart regions :math:`l < |\sigma| < u`
— the only territory where opinions can flip — and each flip is marked
with a cross at the moment it fired::

    viz.traces(traj)

Positions are exact at event times, and between events each action moves
linearly toward its opinion, so what you see is the true piecewise-ballistic
flow of the model, not an interpolation artifact.

Animation
^^^^^^^^^

:func:`~pycoop.viz.animate` turns a trajectory into a
:class:`~matplotlib.animation.FuncAnimation` — the graph with its node
colors evolving event by event::

    anim = viz.animate(traj, stride=5, interval=40)
    anim.save("run.mp4")                    # needs ffmpeg
    anim.save("run.gif", writer="pillow")   # no ffmpeg required

Use ``stride`` to thin long runs; a 100,000-event trajectory does not need
100,000 frames to tell its story. Keep a reference to the animation alive
until it is saved or shown — matplotlib garbage-collects abandoned
animations mid-render.

Scrubbing
^^^^^^^^^

In a notebook, :func:`~pycoop.viz.scrub` gives you a slider over events,
with the graph snapshot on the left and the traces on the right, a dashed
line marking where in the run you're standing::

    viz.scrub(traj)

This requires the ``interactive`` extra (``pip install
'pyCoop[interactive]'``; see :doc:`getting_started`). It is the fastest
way to find the moment a run commits — drag until the flips stop, and
you're looking at the instant the last window shut.
