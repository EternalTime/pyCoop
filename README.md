# pyCoop

A Python library for cooperation games on graphs — agents with continuous
actions and binary opinions negotiating consensus over a network, with
tools for measuring fraughtness, obdurateness, and everything in between.

## Installation

```
git clone https://github.com/EternalTime/pyCoop.git
cd pyCoop
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Requires Python 3.9 or newer (tested on 3.9 through 3.14). Dependencies
(numpy, networkx, matplotlib) are installed automatically; `pip install
'.[interactive]'` enables the in-notebook trajectory scrubber.

The [Getting Started
guide](https://damiansowinski.com/pyCoop/getting_started.html) is the
authority on installation; this section mirrors it.

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

## Testing

From the repository root, with the virtual environment active:

```
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Documentation

The documentation is hosted at
[damiansowinski.com/pyCoop](https://damiansowinski.com/pyCoop/). To build
locally, from the repository root with the virtual environment active:

```
source .venv/bin/activate
pip install -e '.[docs]'
sphinx-build -b html docs docs/_build
```

## License

MIT
