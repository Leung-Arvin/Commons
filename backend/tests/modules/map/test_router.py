# backend/tests/modules/map/test_router.py
import pytest

@pytest.mark.asyncio
async def test_list_maps_empty(client):
    response = await client.get("/api/v1/maps/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_create_and_get_map(client):
    # Create
    payload = {
        "name": "HQ Floor 1",
        "image_url": "/static/floors/hq-1.svg",
        "width_m": 50.0,
        "height_m": 30.0,
    }
    create_resp = await client.post("/api/v1/maps/", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "HQ Floor 1"
    assert "id" in created
    
    # Get
    get_resp = await client.get(f"/api/v1/maps/{created['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "HQ Floor 1"