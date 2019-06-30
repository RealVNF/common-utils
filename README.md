# coord-env-interface
Interface definition between coordination algorithms and environments. Includes a dummy algorithm and environment as example.

## Project structure

* `src/spinterface`: Interface definition between the scale and place algorithm and the environment.
* `src/dummy-algo`: Dummy algorithm implementation.
* `src/dummy-env`: Dummy environment/simulation implementation.

## Interface definition

The main interface definition is described by the `SimulatorInterface` class.

The interface is guided by the gym interface (`gmy.Env`),
The `init()` aligns to the `reset()` function of gym and resets and
initializes the environment with all necessary information including a seed.
The `apply()` function reflects gym's `step()` method:
It sends a placement description for all nodes and
sets the new routing/scheduling.

To pass the information, we utilizes two data classes:
* `SimulatorAction` to pass the scaling and placement to the environment.
* `simulatorState` to report back the current State of the environment.

## Installation

Requires [Python 3.6](https://www.python.org/downloads/release/) and (recommended) [venv](https://docs.python.org/3/library/venv.html).

```bash
python setup.py install
```

## Usage

To use the interface you need to require this module and import the needed classes:

`from spinterface import SimulatorAction, SimulatorInterface, SimulatorState`

For a more detailed explanation take a look into the dummy implementations:
`src/dummy_algo/coordinator.py` and `src/dummy_env/dummy_simulator.py`

### How to run the dummy algorithm against the dummy environment

```bash
dummy-coord -n "res/networks/triangle.graphml" \
            -sf "res/service_functions/abc.yaml" \
            -c "res/config/sim_config.yaml" \
            -i 50
```
For more information look at the [README](src/dummy_algo/README.md) of the dummy algorithm.