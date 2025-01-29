from typing import Sequence
from unittest.mock import MagicMock, patch

import pennylane as qml
import pytest
from compute_api_client import BackendType
from pennylane import DeviceError
from pytest_mock import MockerFixture
from qiskit.exceptions import QiskitError
from qiskit_quantuminspire.qi_backend import QIBackend

with patch("qiskit_quantuminspire.qi_provider.QIProvider"):
    from pennylane_quantuminspire2.qi_device import QI2Device


def test_device_circuit(mocker: MockerFixture, QI2_backend: QIBackend) -> None:
    device = QI2Device(backend=QI2_backend)

    @qml.qnode(device=device)
    # untyped decorator in pennylane, so mypy will complain here
    def quantum_function():  # type: ignore
        qml.Hadamard(wires=[0])
        return qml.expval(qml.PauliX(wires=[0]))

    mock_job = MagicMock()
    mock_submit = MagicMock()
    mock_job.submit = mock_submit
    mocker.patch("qiskit_quantuminspire.qi_backend.QIJob", return_value=mock_job)
    assert quantum_function() is not None
    mock_job.submit.assert_called()


def test_qiskit_error_is_wrapped_as_device_error(mocker: MockerFixture, QI2_backend: QIBackend) -> None:
    # Arrange
    device = QI2Device(backend=QI2_backend)
    error_message = "Result failed ,  Experiment failed. System Message: Simulated Error"
    mocker.patch("pennylane_qiskit.remote.RemoteDevice.execute", side_effect=QiskitError(error_message))

    @qml.qnode(device=device)
    # untyped decorator in pennylane, so mypy will complain here
    def quantum_function():  # type: ignore
        qml.Hadamard(wires=[0])
        return qml.expval(qml.PauliX(wires=[0]))

    # Act & Assert
    with pytest.raises(DeviceError, match=error_message):
        quantum_function()


def test_device_backends(mocker: MockerFixture, backend_repository: Sequence[BackendType]) -> None:
    provider_mock = mocker.Mock()
    provider_mock.backends.return_value = backend_repository
    QI2Device._qi_provider = provider_mock
    # Act
    backends = QI2Device.backends()

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
