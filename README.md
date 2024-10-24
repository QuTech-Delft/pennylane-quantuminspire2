# PennyLane-QuantumInspire Plugin

The PennyLane-QuantumInspire plugin integrates the Quantum Inspire quantum computing backends with PennyLane's quantum machine learning capabilities.

[PennyLane](https://pennylane.readthedocs.io/en/stable/) is a cross-platform Python library for quantum machine learning, automatic differentiation, and optimization of hybrid quantum-classical computations.

[Quantum Inspire] is a platform for quantum computing developed by QuTech.

This plugin relies heavily on the software development kit [(SDK) for the Quantum Inspire platform](https://github.com/QuTech-Delft/quantuminspire)
and the [PennyLane-Qiskit Plugin for Qiskit](https://github.com/PennyLaneAI/pennylane-qiskit).

[Qiskit](https://qiskit.org/documentation/) is an open-source framework for quantum computing.

The Quantum Inspire device is build on top of the Qiskit device. The Quantum Inspire SDK registers a Quantum Inspire
backend to Qiskit to run the algorithms on. This way we combine the strengths and ease of use of the Qiskit plugin
with the computing power of Quantum Inspire backends.

## Features

Grants access to Quantum Inspire's cloud quantum [emulators](https://www.quantum-inspire.com/kbase/emulator-backends/)
and [hardware backends](https://www.quantum-inspire.com/kbase/hardware-backends/).

### Emulator backends

* `QX emulator` - Quantum Inspire emulator run on a commodity cloud-based server, with 4GB RAM. It has a fast turn-around time for simulations up to 26 qubits. For basic users, the commodity cloud-based server will be sufficient.

## Installation

This plugin requires Python version 3.9 and above, as well as PennyLane-Qiskit. Installation of the dependencies can
be done using `pip`:

```bash
pip install pennylane-quantuminspire
```

To ensure your device is working as expected, you can also install the development version from source by cloning
this repository and running a pip install command in the root directory of the repository:

```
git clone https://github.com/QuTech-Delft/pennylane-quantuminspire2.git
cd pennylane-quantuminspire2
pip install -e pluginpath
```

where `pluginpath` is the location of the plugin. It will then be accessible via PennyLane.

## Submitting a Pennylane Circuit

Once a backend has been specified, it may be used to submit circuits.
For example, running a Bell State:

```python
import pennylane as qml
from pennylane_quantuminspire2.qi_device import QI2Device

# Obtain a specific backend by name (get_backends() returns all)
backend = QI2Device.get_backend("Spin")

# create the pennylane device from the desired backend
device = QI2Device(backend=backend)

# Create the quantum function
@qml.qnode(device=device)
def quantum_function():
    qml.Hadamard(wires=[0])
    return qml.expval(qml.PauliX(wires=[0]))

# Run the quantum funciont
print(quantum_function())

```

## Contributing

...

## Running Tests

This package uses the [pytest](https://docs.pytest.org/en/stable/) test runner, and other packages
for mocking interfactions, reporting coverage, etc.
These can be installed with `poetry install`.

To use pytest directly, just run:

```bash
tox -e test
```

## License

[Apache License 2.0].

[quantum inspire]: https://www.quantum-inspire.com/
[apache license 2.0]: https://github.com/PennyLaneAI/pennylane/blob/master/LICENSE
