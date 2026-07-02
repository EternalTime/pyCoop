# pyCoop

A Python library for cooperation games on graphs — agents with continuous
actions and binary opinions negotiating consensus over a network, with
tools for measuring fraughtness, obdurateness, and everything in between.

## Installation

```
git clone https://github.com/EternalTime/pyCoop.git
cd pyCoop
pip install -e .
```

Requires Python 3.9+. Dependencies (numpy, networkx, matplotlib) are
installed automatically; `pip install ipywidgets` enables the in-notebook
trajectory scrubber.

## Modules

| Module               | Description                                                                     |
| -------------------- | ------------------------------------------------------------------------------- |
| `pycoop.graph`       | Graph construction: ERG-until-connected sampling, complete/path/cycle/star/paw  |
| `pycoop.dynamics`    | The update sequence — exact embedded chain with a pluggable inter-event clock   |
| `pycoop.observables` | Agreement, alignment asymmetry, fraughtness, obdurateness, state fractions, α   |
| `pycoop.viz`         | Graph snapshots, action traces, animation, interactive trajectory scrubbing     |

## Example

```python
import pycoop as pc
from pycoop import observables as obs

game = pc.Game(pc.erg_connected(10, 0.1, rng=0), u=0.5, l=0.2, T=0.1)
traj = game.run(rng=1)

sigma, q = traj.final_state()
print(obs.classify(traj.A, sigma))   # consensus | fraught | obdurate
print(obs.state_fractions(traj))     # time-weighted class fractions
```

## Documentation

The documentation is hosted at
[damiansowinski.com/pyCoop](https://damiansowinski.com/pyCoop/). To build
locally: `sphinx-build -b html docs docs/_build` from the repository root.

## License

MIT
