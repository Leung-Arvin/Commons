import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

@pytest.mark.asyncio
async def test_list_assets_empty(client):
    """No assets in DB → empty list."""
    response = await client.get("/api/v1/assets/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_create_and_get_asset(client):
    """Create an asset, then fetch it by ID."""
    # Create
    payload = {
        "name": "Engineer Laptop",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "asset_type": "laptop",
    }
    create_resp = await client.post("/api/v1/assets/", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "Engineer Laptop"
    assert created["mac_address"] == "AA:BB:CC:DD:EE:FF"
    assert "id" in created
    
    # Get by ID
    get_resp = await client.get(f"/api/v1/assets/{created['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Engineer Laptop"

@pytest.mark.asyncio
async def test_get_asset_not_found(client):
    """Fetching a non-existent asset returns 404."""
    fake_id = uuid4()
    response = await client.get(f"/api/v1/assets/{fake_id}")
    assert response.status_code == 404

async def _create_asset(client, mac):
    return (
        await client.post(
            "/api/v1/assets/",
            json={"name": "Laptop", "mac_address": mac, "asset_type": "laptop"},
        )
    ).json()


@pytest.mark.asyncio
async def test_update_asset_partial(client):
    created = await _create_asset(client, "AA:BB:CC:DD:EE:01")
    resp = await client.put(
        f"/api/v1/assets/{created['id']}",
        json={"name": "Renamed Laptop"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Renamed Laptop"
    assert body["asset_type"] == "laptop"  # untouched
    assert body["mac_address"] == "AA:BB:CC:DD:EE:01"


@pytest.mark.asyncio
async def test_update_asset_not_found(client):
    resp = await client.put(f"/api/v1/assets/{uuid4()}", json={"name": "X"})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_asset(client):
    created = await _create_asset(client, "AA:BB:CC:DD:EE:02")
    resp = await client.delete(f"/api/v1/assets/{created['id']}")
    assert resp.status_code == 204
    assert (await client.get(f"/api/v1/assets/{created['id']}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_asset_not_found(client):
    resp = await client.delete(f"/api/v1/assets/{uuid4()}")
    assert resp.status_code == 404


def test_websocket_location_updates():
    """WebSocket should accept connections and broadcast location updates."""
    # Must be synchronous — no @pytest.mark.asyncio
    client = TestClient(app)
    
    with client.websocket_connect("/api/v1/ws/locations") as websocket:
        # Send a test location update
        websocket.send_json({
            "asset_id": "00000000-0000-0000-0000-000000000001",
            "x": 5.0,
            "y": 10.0,
        })
        
        # Should receive the broadcast back
        data = websocket.receive_json()
        assert data["asset_id"] == "00000000-0000-0000-0000-000000000001"
        assert data["x"] == 5.0
        assert data["y"] == 10.0