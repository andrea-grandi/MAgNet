FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

ENV PYTHONUNBUFFERED=1
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8992

EXPOSE 8992

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8992/health')"

CMD ["python", "-m", "translation_mcp.server"]
