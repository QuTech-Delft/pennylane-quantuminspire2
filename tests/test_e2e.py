import pennylane_quantuminspire2  # noqa: F401
from mypyc.common import short_name

from pennylane_quantuminspire2.api.pagination import PageReader
from pennylane_quantuminspire2.api.settings import ApiSettings, AuthSettings, TokenInfo

import pennylane as qml
import numpy as np

async def _fetch_team_member_id(host: str, access_token: str) -> int:
    config = Configuration(host=host, access_token=access_token)
    async with ApiClient(config) as client:
        page_reader = PageReader[PageMember, Member]()
        members_api = MembersApi(client)
        pagination_handler = page_reader.get_single
        members_handler = members_api.read_members_members_get
        member = await pagination_handler(members_handler)
        if member is None:
            raise RuntimeError("Member does not exist")
        return cast(int, member.id)


def _get_auth_tokens() -> None:
    IDP_URL_STAGING = "https://auth.qi2.quantum-inspire.com/realms/oidc_staging"
    QI2_DEFAULT_HOST = "https://staging.qi2.quantum-inspire.com"

    E2E_USERNAME = os.getenv("E2E_USERNAME")
    E2E_PASSWORD = os.getenv("E2E_PASSWORD")

    payload = {
        "grant_type": "password",
        "client_id": "compute-job-manager-direct",
        "username": E2E_USERNAME,
        "password": E2E_PASSWORD,
        "scope": "openid api-access",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    url = f"{IDP_URL_STAGING}/protocol/openid-connect/token"

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()
    token_info = response.json()
    token_info["generated_at"] = time.time()
    host = QI2_DEFAULT_HOST
    member_id = asyncio.run(_fetch_team_member_id(host=host, access_token=token_info["access_token"]))
    auth_settings = AuthSettings(
        client_id="compute-job-manager",
        code_challenge_method="S256",
        code_verifyer_length=64,
        well_known_endpoint=f"{IDP_URL_STAGING}/.well-known/openid-configuration",
        tokens=None,
        team_member_id=member_id,
    )

    dir_path = Path.home().joinpath(".quantuminspire")
    dir_path.mkdir(parents=True, exist_ok=True)

    ApiSettings(auths={host: auth_settings}, default_host=host).store_tokens(host=host, tokens=TokenInfo(**token_info))


def _run_e2e_tests(name: str) -> None:
    e2e_device = qml.device("quantum_inspire.{}".format(name), wires=2, shots=10)

    # Step 2: Create a quantum circuit
    @qml.qnode(e2e_device)
    def my_quantum_circuit(params):
        qml.RX(params[0], wires=0)  # Apply an RX gate to qubit 0
        qml.RY(params[1], wires=1)  # Apply an RY gate to qubit 1
        qml.CNOT(wires=[0, 1])  # Apply a CNOT gate
        return qml.expval(qml.PauliZ(0))  # Measure the expectation value of PauliZ on qubit 0

    # Step 3: Initialize some parameters
    params = np.array([0.1, 0.2])

    # Step 4: Execute the circuit
    result = my_quantum_circuit(params)
    print(f"Expectation value: {result}")

    # Step 5: Perform optimization (optional)
    # For example, use gradient descent to minimize the output
    opt = qml.GradientDescentOptimizer(stepsize=0.1)
    for i in range(100):
        params = opt.step(my_quantum_circuit, params)

def main(name: str) -> None:
    _get_auth_tokens()
    _run_e2e_tests(name=name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E2E test on a backend.")
    parser.add_argument(
        "name",
        type=str,
        help="Name of the backend where the E2E tests will run.",
    )

    args = parser.parse_args()
    # main(args.name)
    pass
