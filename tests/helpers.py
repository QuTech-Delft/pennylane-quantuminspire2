import asyncio
import os
import requests

from datetime import time

from compute_api_client import ApiClient, Configuration, Member, MembersApi, PageMember
from qiskit_quantuminspire.api.settings import ApiSettings, AuthSettings, TokenInfo

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
