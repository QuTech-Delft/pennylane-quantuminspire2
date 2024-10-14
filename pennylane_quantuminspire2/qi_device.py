import pennylane as qml
from pennylane import numpy as np

class QIDevice(qml.QubitDevice):
    name = 'Qubit Device for Quantum Inspire 2'
    short_name = 'custom.qubit'
    pennylane_requires = '>=0.23'
    version = '0.0.1'
    author = 'QuTech'

    operations = {"RX", "RY", "RZ", "PhaseShift"}
    observables = {"PauliX", "PauliZ"}
