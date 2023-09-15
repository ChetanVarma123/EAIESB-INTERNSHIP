import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


async def test_get_departments():
    response = await client.get("/departments")
    assert response.status_code == 200
    assert response.json() == [
        {
            "departmentName": "CSE",
            "id": "650291aa5d39d878727e0c0e"
        },
        {
            "departmentName": "ECE",
            "id": "650291c65d39d878727e0c0f"
        },
        {
            "departmentName": "CSE-ROBOTICS",
            "id": "65029d7769e3b110582515d0"
        }
    ]
if __name__ == "__main__":
    asyncio.run(test_get_departments())