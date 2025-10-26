"""A2A Client for communicating with other agents."""

import logging
import httpx
import asyncio
import uuid

from typing import Optional, Dict, Any
from a2a.client import ClientFactory, ClientConfig, A2ACardResolver, A2AClient as LibA2AClient
from a2a.types import TextPart, Message, Role, AgentCard, MessageSendParams, SendMessageRequest
from a2a.utils.constants import EXTENDED_AGENT_CARD_PATH

logger = logging.getLogger(__name__)


class A2AClient:
    """Client for communicating with specialized agents via A2A protocol."""
    
    def __init__(self, agent_url: str, agent_name: str, max_retries: int = 5, base_delay: float = 1.0):
        """Initialize the A2A client for a specific agent.
        
        Args:
            agent_url: The base URL of the agent's A2A server
            agent_name: Name of the agent for logging purposes
            max_retries: Maximum number of connection retry attempts (default: 5)
            base_delay: Base delay in seconds for exponential backoff (default: 1.0)
        """

        if not agent_url:
            raise ValueError("agent_url must be provided")
        
        self.agent_url = agent_url
        self.agent_name = agent_name
        self.client = None
        self.httpx_client = httpx.AsyncClient(timeout=30.0)
        self.max_retries = max_retries
        self.base_delay = base_delay
        logger.info(f"[A2A CLIENT] Will connect to {agent_name} at {agent_url}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _ensure_client(self) -> None:
        """Ensure the client is initialized."""
        if self.client:
            return 
        
        resolver = A2ACardResolver(httpx_client=self.httpx_client, base_url=self.agent_url)
        card = await resolver.get_agent_card()
        if getattr(card, "supports_authenticated_extended_card", False):
            try:
                card = await resolver.get_agent_card(
                    relative_card_path=EXTENDED_AGENT_CARD_PATH,
                    http_kwargs={"headers": {"Authorization": "Bearer dummy-token"}},
                )
            except Exception as e:
                pass

        self._agent_card = card
        self._a2a_client = LibA2AClient(httpx_client=self.httpx_client, agent_card=card)

    async def get_agent_card(self) -> Optional[Dict[str, Any]]:
        try:   
            await self._ensure_client()
            return self._agent_card.model_dump(exclude_none=True) if self._agent_card else None
        except Exception as e:
            print(f"Error getting agent card from {self.agent_name} at {self.agent_url}: {str(e)}")
            return None
        
    async def send_message(self, text: str, conversation_id: Optional[str] = None) -> str:
        await self._ensure_client()
        assert self._a2a_client is not None, "A2A client is not initialized"

        params_dict: Dict[str, Any] = {
            "message": {
                "role": "user",
                "messageId": uuid.uuid4().hex,
                "conversationId": conversation_id,
                "parts": [{"kind": "text", "text": text}],
            }
        }

        try:
            print(f"[A2A CLIENT][send_message] Sending message to {self.agent_name} at {self.agent_url}")
            print(f"[A2A CLIENT][send_message] Agent card endpoints: {self._agent_card.model_dump() if hasattr(self, '_agent_card') else 'N/A'}")
            request = SendMessageRequest(id=str(uuid.uuid4()), params=MessageSendParams(**params_dict))
            print(f"[A2A CLIENT][send_message] Request: {request.model_dump()}")
            resp = await self._a2a_client.send_message(request)
            print(f"[A2A CLIENT][send_message] Response received successfully")
            data = resp.model_dump(mode="json", exclude_none=True)

            print("Especialista respondeu:")
            print(data)

            result = data.get("result") or {}
            parts = []
            if isinstance(result, dict) and result.get("kind") == "message" and "parts" in result:
                parts = result.get("parts") or []

            if not parts and isinstance(result, dict):
                status = result.get("status") or {}
                message = status.get("message") or {}
                parts = message.get("parts") or []

            for part in parts:
                if part.get("kind") == "text":
                    return part.get("text", "Empty response from agent.")

            return "Unexpected response format from the specialist agent."

        except httpx.HTTPStatusError as e:
            print(f"[A2A CLIENT][send_message][ERROR] HTTPStatusError: {e.response.status_code}")
            print(f"[A2A CLIENT][send_message][ERROR] Response text: {e.response.text}")
            print(f"[A2A CLIENT][send_message][ERROR] Request URL: {e.request.url}")
            return f"Communication error with agent at {self.agent_url}: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            print(f"[A2A CLIENT][send_message][ERROR] Exception: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"[A2A CLIENT][send_message][ERROR] Traceback: {traceback.format_exc()}")
            return f"Unexpected error calling agent: {str(e)}"

    async def close(self):
        await self.httpx_client.aclose()