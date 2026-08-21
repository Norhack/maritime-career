import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.main import health


def test_health_returns_ok_status():
    response = asyncio.run(health())
    assert response.status_code == 200
    assert response.body == b'{"status":"ok"}'
