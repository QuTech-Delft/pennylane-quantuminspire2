from typing import Sequence

import pennylane as qml
from compute_api_client import BackendType
from pytest_mock import MockerFixture
from qiskit_quantuminspire.qi_backend import QIBackend

from pennylane_quantuminspire2.qi_device import QI2Device


def test_device_circuit(mocker: MockerFixture, QI2_backend: QIBackend) -> None:
    device = QI2Device(backend=QI2_backend)

    @qml.qnode(device=device)
    # untyped decorator in pennylane, so mypy will complain here
    def quantum_function():  # type: ignore
        qml.Hadamard(wires=[0])
        return qml.expval(qml.PauliX(wires=[0]))

    mocker.patch("qiskit_quantuminspire.qi_backend.QIJob")
    assert quantum_function() is not None


def test_device_backends(mocker: MockerFixture, backend_repository: Sequence[BackendType]) -> None:
    provider_mock = mocker.Mock()
    provider_mock.backends.return_value = backend_repository
    QI2Device._qi_provider = provider_mock
    # Act
    backends = QI2Device.get_backends()

    # Assert
    provider_mock.backends.assert_called_once()
    assert len(backends) == 2


def test_device_backend(mocker: MockerFixture, backend_repository: Sequence[BackendType]) -> None:
    provider_mock = mocker.Mock()
    provider_mock.get_backend.return_value = backend_repository
    QI2Device._qi_provider = provider_mock
    # Act
    backend = QI2Device.get_backend(name="qi_backend_10")

    # Assert
    provider_mock.get_backend.assert_called_once()
    assert backend is not None
