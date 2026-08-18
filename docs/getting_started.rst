Getting Started
===============

In this guide you will install pyCoop and watch your first cooperation game
play out. The library rests on numpy, networkx, and matplotlib — nothing
exotic — so the install is quick.

Installation
^^^^^^^^^^^^

pyCoop requires Python 3.9 or newer, and is tested on 3.9 through 3.14.
Install it into a virtual environment — Homebrew and other
distribution-managed Pythons refuse system-wide installs (:pep:`668`),
and ``pip`` is often available only as ``pip3`` outside a virtual
environment::

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install git+https://github.com/EternalTime/pyCoop

or clone and install in editable mode if you plan to poke at the source::

    git clone https://github.com/EternalTime/pyCoop.git
    cd pyCoop
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e .

For the in-notebook trajectory scrubber you'll also want
``pip install 'pyCoop[interactive]'``. Check the install::

    >>> import pycoop

To run the test suite, or to build these docs, install the matching extra
from a clone with the environment active::

    source .venv/bin/activate
    pip install -e '.[test]'
    pytest

    pip install -e '.[docs]'
    sphinx-build -b html docs docs/_build

First game
^^^^^^^^^^

The paw — a triangle with a pendant tail — is the smallest graph that can
trap a group in a fraught state, which makes it the right first playground.
Build the graph, set the thresholds, and run::

    import pycoop as pc
    from pycoop import observables as obs

    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=7)

    sigma, q = traj.final_state()
    print(obs.classify(traj.A, sigma))
    print(f"absorbed at t = {traj.t_end:.1f} after {traj.steps} events")

Three parameters govern everything. The agreement threshold ``u`` is an
upper limit — a player can only reconsider while their local mean action
is inside :math:`(-u, u)`. The position threshold ``l`` is a lower limit,
keeping fence-sitters from flipping — a player must be committed,
:math:`|\sigma_j| > l`, before a change of heart is allowed. And ``T``
sets the tempo: the mean wait between decision events across the whole
network is :math:`T/N`.

Now look at what happened::

    from pycoop import viz
    import matplotlib.pyplot as plt

    viz.traces(traj)
    plt.show()

Each curve is one player's action drifting toward its opinion; the shaded
bands are the change-of-heart regions :math:`l < |\sigma| < u`, and the
crosses mark opinion flips. To see the same run as a movie on the graph::

    anim = viz.animate(traj, stride=5)
    anim.save("paw.gif", writer="pillow")

Run it a few more times with different seeds. Sometimes the paw finds
consensus quickly; sometimes it lands in the fraught trap where the pendant
single-handedly holds the hub against the pull of the two free vertices.
How often each happens, and why, is the subject of the next two guides.
