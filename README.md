# pyCoop

Cooperation games on graphs. Each agent carries a continuous action and a
binary opinion, and the group negotiates consensus over a network. pyCoop
runs the dynamics and measures what comes out.

## Installation

```
git clone https://github.com/EternalTime/pyCoop.git
cd pyCoop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Requires Python 3.9 or newer (tested on 3.9 through 3.14). numpy,
networkx, and matplotlib install automatically; `pip install
'.[interactive]'` adds the in-notebook trajectory scrubber. The [Getting
Started guide](https://damiansowinski.com/pyCoop/getting_started.html) is
the authority on installation, and this section mirrors it.

## Modules

| Module               | Description                                                                    |
| -------------------- | ------------------------------------------------------------------------------ |
| `pycoop.graph`       | ERG-until-connected sampling, complete/path/cycle/star/paw                     |
| `pycoop.dynamics`    | The exact embedded chain, with a pluggable inter-event clock                   |
| `pycoop.observables` | Agreement, alignment asymmetry, fraughtness, obdurateness, state fractions, α  |
| `pycoop.viz`         | Snapshots, action traces, animation, interactive scrubbing                     |

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

From the repository root:

```
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Documentation

Hosted at [damiansowinski.com/pyCoop](https://damiansowinski.com/pyCoop/),
and built from the repository root with:

```
source .venv/bin/activate
pip install -e '.[docs]'
sphinx-build -b html docs docs/_build
```

## License

MIT
