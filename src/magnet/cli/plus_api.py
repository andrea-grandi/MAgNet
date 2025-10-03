from urllib.parse import urljoin

import requests

from magnet.cli.config import Settings
from magnet.cli.constants import DEFAULT_MAGNET_ENTERPRISE_URL
from magnet.cli.version import get_magnet_version


class PlusAPI:
    """
    This class exposes methods for working with the Magnet+ API.
    """

    TOOLS_RESOURCE = "/magnet_plus/api/v1/tools"
    ORGANIZATIONS_RESOURCE = "/magnet_plus/api/v1/me/organizations"
    NETS_RESOURCE = "/magnet_plus/api/v1/nets"
    AGENTS_RESOURCE = "/magnet_plus/api/v1/agents"
    TRACING_RESOURCE = "/magnet_plus/api/v1/tracing"
    EPHEMERAL_TRACING_RESOURCE = "/magnet_plus/api/v1/tracing/ephemeral"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"Magnet-CLI/{get_magnet_version()}",
            "X-Magnet-Version": get_magnet_version(),
        }
        settings = Settings()
        if settings.org_uuid:
            self.headers["X-Magnet-Organization-Id"] = settings.org_uuid

        self.base_url = (
            str(settings.enterprise_base_url) or DEFAULT_MAGNET_ENTERPRISE_URL
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self.base_url, endpoint)
        session = requests.Session()
        session.trust_env = False
        return session.request(method, url, headers=self.headers, **kwargs)

    def login_to_tool_repository(self):
        return self._make_request("POST", f"{self.TOOLS_RESOURCE}/login")

    def get_tool(self, handle: str):
        return self._make_request("GET", f"{self.TOOLS_RESOURCE}/{handle}")

    def get_agent(self, handle: str):
        return self._make_request("GET", f"{self.AGENTS_RESOURCE}/{handle}")

    def publish_tool(
        self,
        handle: str,
        is_public: bool,
        version: str,
        description: str | None,
        encoded_file: str,
        available_exports: list[str] | None = None,
    ):
        params = {
            "handle": handle,
            "public": is_public,
            "version": version,
            "file": encoded_file,
            "description": description,
            "available_exports": available_exports,
        }
        return self._make_request("POST", f"{self.TOOLS_RESOURCE}", json=params)

    def deploy_by_name(self, project_name: str) -> requests.Response:
        return self._make_request(
            "POST", f"{self.NETS_RESOURCE}/by-name/{project_name}/deploy"
        )

    def deploy_by_uuid(self, uuid: str) -> requests.Response:
        return self._make_request("POST", f"{self.NETS_RESOURCE}/{uuid}/deploy")

    def net_status_by_name(self, project_name: str) -> requests.Response:
        return self._make_request(
            "GET", f"{self.NETS_RESOURCE}/by-name/{project_name}/status"
        )

    def net_status_by_uuid(self, uuid: str) -> requests.Response:
        return self._make_request("GET", f"{self.NETS_RESOURCE}/{uuid}/status")

    def net_by_name(
        self, project_name: str, log_type: str = "deployment"
    ) -> requests.Response:
        return self._make_request(
            "GET", f"{self.NETS_RESOURCE}/by-name/{project_name}/logs/{log_type}"
        )

    def net_by_uuid(
        self, uuid: str, log_type: str = "deployment"
    ) -> requests.Response:
        return self._make_request(
            "GET", f"{self.NETS_RESOURCE}/{uuid}/logs/{log_type}"
        )

    def delete_net_by_name(self, project_name: str) -> requests.Response:
        return self._make_request(
            "DELETE", f"{self.NETS_RESOURCE}/by-name/{project_name}"
        )

    def delete_net_by_uuid(self, uuid: str) -> requests.Response:
        return self._make_request("DELETE", f"{self.NETS_RESOURCE}/{uuid}")

    def list_nets(self) -> requests.Response:
        return self._make_request("GET", self.NETS_RESOURCE)

    def create_net(self, payload) -> requests.Response:
        return self._make_request("POST", self.NETS_RESOURCE, json=payload)

    def get_organizations(self) -> requests.Response:
        return self._make_request("GET", self.ORGANIZATIONS_RESOURCE)

    def initialize_trace_batch(self, payload) -> requests.Response:
        return self._make_request(
            "POST",
            f"{self.TRACING_RESOURCE}/batches",
            json=payload,
            timeout=30,
        )

    def initialize_ephemeral_trace_batch(self, payload) -> requests.Response:
        return self._make_request(
            "POST",
            f"{self.EPHEMERAL_TRACING_RESOURCE}/batches",
            json=payload,
        )

    def send_trace_events(self, trace_batch_id: str, payload) -> requests.Response:
        return self._make_request(
            "POST",
            f"{self.TRACING_RESOURCE}/batches/{trace_batch_id}/events",
            json=payload,
            timeout=30,
        )

    def send_ephemeral_trace_events(
        self, trace_batch_id: str, payload
    ) -> requests.Response:
        return self._make_request(
            "POST",
            f"{self.EPHEMERAL_TRACING_RESOURCE}/batches/{trace_batch_id}/events",
            json=payload,
            timeout=30,
        )

    def finalize_trace_batch(self, trace_batch_id: str, payload) -> requests.Response:
        return self._make_request(
            "PATCH",
            f"{self.TRACING_RESOURCE}/batches/{trace_batch_id}/finalize",
            json=payload,
            timeout=30,
        )

    def finalize_ephemeral_trace_batch(
        self, trace_batch_id: str, payload
    ) -> requests.Response:
        return self._make_request(
            "PATCH",
            f"{self.EPHEMERAL_TRACING_RESOURCE}/batches/{trace_batch_id}/finalize",
            json=payload,
            timeout=30,
        )

    def mark_trace_batch_as_failed(
        self, trace_batch_id: str, error_message: str
    ) -> requests.Response:
        return self._make_request(
            "PATCH",
            f"{self.TRACING_RESOURCE}/batches/{trace_batch_id}",
            json={"status": "failed", "failure_reason": error_message},
            timeout=30,
        )
