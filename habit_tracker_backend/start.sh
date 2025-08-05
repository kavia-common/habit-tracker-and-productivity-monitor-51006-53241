#!/bin/bash
# Entrypoint script to launch the FastAPI app on port 3001
# Usage: bash start.sh or chmod +x start.sh && ./start.sh

exec uvicorn src.api.main:app --host 0.0.0.0 --port 3001
