from unittest.mock import AsyncMock, MagicMock
from pytest_mock import MockerFixture
import pytest
import pennylane as qml
from pennylane_quantuminspire2.qi_device import QI2Device
from qiskit_quantuminspire.qi_backend import QIBackend

def test_device_circuit(
    mocker: MockerFixture,
    QI2_backend: QIBackend
):
    device = QI2Device(backend=QI2_backend)
    @qml.qnode(device=device)
    def quantum_function():
        qml.Hadamard(wires=[0])
        return qml.expval(qml.PauliX(wires=[0]))

    mocker.patch("qiskit_quantuminspire.qi_backend.QIJob")
    assert quantum_function() is not None


