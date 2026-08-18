Getting Started
===============

Here you will install pyCoop and run your first cooperation game.

Installation
^^^^^^^^^^^^

pyCoop requires Python 3.9 or newer, and is tested on 3.9 through 3.14.
Install it into a virtual environment: distribution-managed Pythons refuse
system-wide installs (:pep:`668`), and ``pip`` is often available only as
``pip3`` outside one::

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

The in-notebook trajectory scrubber needs
``pip install 'pyCoop[interactive]'``. Check the install::

    >>> import pycoop

The tests and these docs each have their own extra, installed from a
clone with the environment active::

    source .venv/bin/activate
    pip install -e '.[test]'
    pytest

    pip install -e '.[docs]'
    sphinx-build -b html docs docs/_build

First game
^^^^^^^^^^

The paw - a triangle with a pendant tail - is the smallest graph that can
trap a group in a fraught state, so build it, set the thresholds, and
run::

    import pycoop as pc
    from pycoop import observables as obs

    game = pc.Game(pc.paw(), u=0.5, l=0.2, T=1.0)
    traj = game.run(rng=7)

    sigma, q = traj.final_state()
    print(obs.classify(traj.A, sigma))
    print(f"absorbed at t = {traj.t_end:.1f} after {traj.steps} events")

Three parameters govern everything. The agreement threshold ``u`` lets a
player reconsider only while their local mean action lies inside
:math:`(-u, u)`, and the position threshold ``l`` lets them do it only
once committed, :math:`|\sigma_j| > l`, which keeps fence-sitters from
flipping. The third, ``T``, sets the tempo: the mean wait between decision
events across the network is :math:`T/N`. See :doc:`guide_dynamics` for
the rules in full.

Now look at what happened::

    from pycoop import viz
    import matplotlib.pyplot as plt

    viz.traces(traj)
    plt.show()

Each curve is one player's action drifting toward its opinion, the shaded
bands are the change-of-heart regions :math:`l < |\sigma| < u`, and the
crosses mark flips. Or watch the run as a movie on the graph::

    anim = viz.animate(traj, stride=5)
    anim.save("paw.gif", writer="pillow")

Run it again with other seeds. Sometimes the paw finds consensus quickly,
sometimes it lands in the fraught trap where the pendant single-handedly
holds the hub against the two free vertices. How often each happens, and
why, is the subject of the next two guides.
