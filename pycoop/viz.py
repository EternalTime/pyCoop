"""Visualization: graph snapshots, trajectory traces, animation, scrubbing.

Actions color the nodes (diverging colormap over [-1, 1]); opinions set
the node border (dark = +1, light = -1).  Change-of-heart bands
[l, u] and [-u, -l] are shaded in trace plots.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as manim
import networkx as nx
import numpy as np

from .graph import as_graph

__all__ = ["snapshot", "traces", "animate", "scrub"]

_POS_EDGE = "#1a1a1a"   # opinion +1 border
_NEG_EDGE = "#b0b0b0"   # opinion -1 border


def _layout(G, pos=None, seed=0):
    return pos if pos is not None else nx.spring_layout(G, seed=seed)


def snapshot(G, sigma, q=None, ax=None, pos=None, cmap="coolwarm",
             node_size=300, colorbar=False):
    """Draw the graph with nodes colored by action and, if given,
    bordered by opinion.  Returns (ax, pos)."""
    G = as_graph(G)
    pos = _layout(G, pos)
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 4))
    sigma = np.asarray(sigma, float)
    edgecolors = None
    if q is not None:
        edgecolors = [_POS_EDGE if qi > 0 else _NEG_EDGE for qi in q]
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5)
    nodes = nx.draw_networkx_nodes(
        G, pos, ax=ax, node_color=sigma, cmap=cmap, vmin=-1, vmax=1,
        node_size=node_size, edgecolors=edgecolors, linewidths=2.0,
    )
    if colorbar:
        plt.colorbar(nodes, ax=ax, label=r"$\sigma$")
    ax.set_axis_off()
    return ax, pos


def traces(traj, players=None, ax=None, bands=True, flips=True,
           cmap="tab10", lw=1.2):
    """Action time series sigma_i(t) with change-of-heart bands and flip
    markers.  Positions are exact at event times; segments between are
    drawn straight (exact up to wall clipping within an interval)."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 4))
    n = traj.n
    players = range(n) if players is None else players
    colors = plt.get_cmap(cmap)
    l, u = traj.params["l"], traj.params["u"]
    if bands:
        for lo, hi in ((l, u), (-u, -l)):
            ax.axhspan(lo, hi, color="0.85", zorder=0)
    for i in players:
        ax.plot(traj.t, traj.sigma[:, i], color=colors(i % 10), lw=lw,
                label=f"{i}")
    if flips:
        k = np.nonzero(traj.flipped)[0]
        ax.scatter(traj.t[k + 1], traj.sigma[k + 1, traj.player[k]],
                   marker="x", s=30, color="k", zorder=5)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\sigma_i$")
    ax.set_ylim(-1.05, 1.05)
    if len(list(players)) <= 10:
        ax.legend(title="player", fontsize=8, ncol=2)
    return ax


def animate(traj, G=None, pos=None, stride=1, interval=50,
            cmap="coolwarm", node_size=300):
    """FuncAnimation over trajectory frames (every `stride` events).

    Returns the animation; save with ``anim.save("run.mp4")`` (needs
    ffmpeg) or ``anim.save("run.gif", writer="pillow")``.  Keep a
    reference alive until saved/shown.
    """
    G = as_graph(traj.A if G is None else G)
    pos = _layout(G, pos)
    frames = range(0, traj.sigma.shape[0], stride)
    fig, ax = plt.subplots(figsize=(5, 4))
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5)
    nodes = nx.draw_networkx_nodes(
        G, pos, ax=ax, node_color=traj.sigma[0], cmap=cmap, vmin=-1, vmax=1,
        node_size=node_size, linewidths=2.0,
        edgecolors=[_POS_EDGE if qi > 0 else _NEG_EDGE for qi in traj.q[0]],
    )
    ax.set_axis_off()
    title = ax.set_title(f"t = {traj.t[0]:.2f}")

    def update(k):
        nodes.set_array(traj.sigma[k])
        nodes.set_edgecolor(
            [_POS_EDGE if qi > 0 else _NEG_EDGE for qi in traj.q[k]])
        title.set_text(f"t = {traj.t[k]:.2f}")
        return nodes, title

    return manim.FuncAnimation(fig, update, frames=frames,
                               interval=interval, blit=False)


def scrub(traj, G=None, pos=None, cmap="coolwarm", node_size=300):
    """Interactive in-notebook frame scrubber (requires ipywidgets)."""
    try:
        from ipywidgets import IntSlider, interact
    except ImportError as e:
        raise ImportError(
            "scrub requires ipywidgets: pip install 'pyCoop[interactive]'"
        ) from e
    G = as_graph(traj.A if G is None else G)
    pos = _layout(G, pos)
    kmax = traj.sigma.shape[0] - 1

    def show(k=0):
        fig, (axg, axt) = plt.subplots(
            1, 2, figsize=(11, 4), gridspec_kw={"width_ratios": [1, 1.6]})
        snapshot(G, traj.sigma[k], traj.q[k], ax=axg, pos=pos,
                 cmap=cmap, node_size=node_size)
        traces(traj, ax=axt)
        axt.axvline(traj.t[k], color="k", ls="--", lw=1)
        axg.set_title(f"event {k}, t = {traj.t[k]:.2f}")
        plt.show()

    return interact(show, k=IntSlider(0, 0, kmax, 1))
