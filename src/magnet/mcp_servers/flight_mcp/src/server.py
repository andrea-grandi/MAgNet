import os

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from dotenv import load_dotenv

from .logic import get_flight_info
from .models import FlightInfoInput, FlightInfoOutput

load_dotenv()

HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8787"))

mcp = FastMCP(
    name="flight_mcp",
    instructions=(
        "MCP server for flight information."
        "Main tools: get_flight_info_tool"
        "The response includes information about flights, such as schedules, status, and boarding windows."
    ),
)

@mcp.resource("flight://specs")
def specs(context: Context) -> dict:
    return {
        "provider": "FlightInfoAPI",
        "inputs": {"flight_id": "str"}
    }

@mcp.tool
async def get_flight_info_tool(context: Context, payload: FlightInfoInput) -> FlightInfoOutput:
    try:
        if not payload.city or not payload.date:
            raise ToolError("City and date are required fields.")

        out = await get_flight_info(payload)

        await context.info(
            "flight_mcp.accu.forecast.ok",
            extra={"status": out.status, "departure": out.departure, "arrival": out.arrival, "duration": out.duration},
        )
        return out

    except ToolError:
        await context.error("flight_mcp.accu.forecast.tool_error")
        raise
    except Exception as e:
        await context.error("flight_mcp.accu.forecast.unexpected")
        raise ToolError(f"Internal API failure: {type(e).__name__}: {e}")

@mcp.tool
def health_check() -> dict:
    """Health check endpoint for Docker"""
    return {"status": "healthy", "service": "flight-mcp"}


if __name__ == "__main__":
    mcp.run(transport="http", host=HOST, port=PORT, path="/mcp")