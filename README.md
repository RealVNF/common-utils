# common-utils
Interface definition between coordination algorithms and environments. Includes a dummy environment as example.

## Project structure

* `src/spinterface`: Interface definition between the scale and place algorithm and the environment.
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

### Interface

To use the interface you need to require this module and import the needed classes:

`from spinterface import SimulatorAction, SimulatorInterface, SimulatorState`


### Dummy environment

To use the dummy environment use:

`from dummy_env import DummySimulator as Simulator`
