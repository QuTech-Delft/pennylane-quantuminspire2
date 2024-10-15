import pytest
from qiskit_quantuminspire.qi_backend import QIBackend
from compute_api_client import BackendStatus, BackendType

@pytest.fixture
def QI2_backend() -> BackendType:
    """ Backend fixture for fields we care about."""
    backend_type = BackendType(
        name="qi_backend",
        nqubits=3,
        gateset=["x", "sdag", "prep_y", "measure_z", "h"],
        topology=[[0, 1], [1, 2], [2, 0]],
        id=1,
        is_hardware=True,
        image_id="qi_backend",
        features=[],
        default_compiler_config="",
        status=BackendStatus.IDLE,
        default_number_of_shots=1024,
        max_number_of_shots=2048,
        infrastructure="QCI",
        description="A Quantum Inspire backend",
        native_gateset="",
    )
    return QIBackend(backend_type=backend_type)
