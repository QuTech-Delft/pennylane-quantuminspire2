from typing import Sequence

import pytest
from compute_api_client import BackendStatus, BackendType
from qiskit_quantuminspire.qi_backend import QIBackend


def create_backend(id: int = 1, name: str = "qi_backend") -> BackendType:
    backend_type = BackendType(
        name=name,
        nqubits=3,
        gateset=["x", "sdag", "prep_y", "measure_z", "h"],
        topology=[[0, 1], [1, 2], [2, 0]],
        id=id,
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


@pytest.fixture
def QI2_backend() -> BackendType:
    """Backend fixture for fields we care about."""
    return create_backend()


@pytest.fixture
def backend_repository() -> Sequence[BackendType]:
    return [
        create_backend(),
        create_backend(10, "qi_backend_10"),
    ]
