from typing import Sequence
from unittest.mock import AsyncMock

import pytest
from compute_api_client import BackendStatus, BackendType
from pytest_mock import MockerFixture
from qiskit_quantuminspire.api.pagination import PageReader
from qiskit_quantuminspire.qi_backend import QIBackend


@pytest.fixture
def page_reader_mock(mocker: MockerFixture) -> AsyncMock:
    # Simply calling mocker.patch() doesn't work because PageReader is a generic class
    page_reader_mock = AsyncMock()
    page_reader_mock.get_all = AsyncMock()
    page_reader_mock.get_single = AsyncMock()
    mocker.patch.object(PageReader, "get_all", page_reader_mock.get_all)
    mocker.patch.object(PageReader, "get_single", page_reader_mock.get_single)
    return page_reader_mock


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
def backend_repository(page_reader_mock: AsyncMock) -> Sequence[BackendType]:
    return [
        create_backend(),
        create_backend(10, "qi_backend_10"),
    ]
