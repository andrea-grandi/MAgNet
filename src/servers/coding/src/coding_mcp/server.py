"""FastMCP server for coding operations."""

import os
import logging

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from dotenv import load_dotenv

from .models import (
    CodeGenerationInput,
    CodeGenerationOutput,
    CodeReviewInput,
    CodeReviewOutput,
    CodeDebugInput,
    CodeDebugOutput
)
from .logic import generate_code, review_code, debug_code

logger = logging.getLogger(__name__)

if load_dotenv():
    print("Loaded .env file")
else:
    print("No .env file found")

HOST = os.getenv("MCP_HOST", "localhost")
PORT = int(os.getenv("MCP_PORT", "8991"))

mcp = FastMCP(
    name="coding_mcp",
    instructions=(
        "This MCP provides tools for code generation, code review, and debugging. "
        "It can generate code from descriptions, review code quality, and help debug issues."
    ),
)


@mcp.tool
def code_generation_tool(ctx: Context, req: CodeGenerationInput) -> CodeGenerationOutput:
    """Generate code based on a description."""
    
    try:
        return generate_code(req)
    except Exception as e:
        logger.info(f"Exception in code generation: {e}")
        raise ToolError(str(e))


@mcp.tool
def code_review_tool(ctx: Context, req: CodeReviewInput) -> CodeReviewOutput:
    """Review code and provide quality feedback."""
    
    try:
        return review_code(req)
    except Exception as e:
        logger.info(f"Exception in code review: {e}")
        raise ToolError(str(e))


@mcp.tool
def code_debug_tool(ctx: Context, req: CodeDebugInput) -> CodeDebugOutput:
    """Debug code and suggest fixes."""
    
    try:
        return debug_code(req)
    except Exception as e:
        logger.info(f"Exception in code debug: {e}")
        raise ToolError(str(e))


@mcp.tool
def health_check() -> dict:
    """Health check endpoint for Docker"""
    
    return {"status": "healthy", "service": "coding-mcp"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=HOST, port=PORT, path="/mcp")
