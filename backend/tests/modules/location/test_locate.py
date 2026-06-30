# backend/tests/modules/location/test_locate.py
import pytest
from uuid import uuid4


async def _setup_floor_with_aps(client):
    fp = (
        await client.post(
            "/api/v1/maps/",
            json={"name": "F", "building": "B", "floor": "1", "width": 100, "height": 100},
        )
    ).json()
    for mac, x, y in [("AA:00", 0, 0), ("AA:01", 10, 0), ("AA:02", 0, 10)]:
        await client.post(
            f"/api/v1/maps/{fp['id']}/aps",
            json={"mac_address": mac, "x": x, "y": y},
        )
    return fp


async def _create_asset(client, mac="DE:AD:BE:EF:00:01"):
    return (
        await client.post("/api/v1/assets/", json={"name": "L", "mac_address": mac})
    ).json()


@pytest.mark.asyncio
async def test_locate_asset_persists_position(client):
    fp = await _setup_floor_with_aps(client)
    asset = await _create_asset(client)
    payload = {
        "floor_plan_id": fp["id"],
        "readings": [
            {"mac_address": "AA:00", "rssi": -40},
            {"mac_address": "AA:01", "rssi": -60},
            {"mac_address": "AA:02", "rssi": -60},
        ],
    }
    resp = await client.post(f"/api/v1/assets/{asset['id']}/locate", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["last_x"] is not None
    assert body["last_y"] is not None
    assert body["last_floor_id"] == fp["id"]
    assert body["last_seen_at"] is not None


@pytest.mark.asyncio
async def test_locate_position_reflected_in_get(client):
    fp = await _setup_floor_with_aps(client)
    asset = await _create_asset(client)
    locate = await client.post(
        f"/api/v1/assets/{asset['id']}/locate",
        json={
            "floor_plan_id": fp["id"],
            "readings": [
                {"mac_address": "AA:00", "rssi": -40},
                {"mac_address": "AA:01", "rssi": -60},
                {"mac_address": "AA:02", "rssi": -60},
            ],
        },
    )
    expected = locate.json()
    fetched = (await client.get(f"/api/v1/assets/{asset['id']}")).json()
    assert fetched["last_x"] == expected["last_x"]
    assert fetched["last_y"] == expected["last_y"]
    assert fetched["last_floor_id"] == fp["id"]


@pytest.mark.asyncio
async def test_locate_insufficient_readings_returns_422(client):
    fp = await _setup_floor_with_aps(client)
    asset = await _create_asset(client)
    resp = await client.post(
        f"/api/v1/assets/{asset['id']}/locate",
        json={
            "floor_plan_id": fp["id"],
            "readings": [
                {"mac_address": "AA:00", "rssi": -40},
                {"mac_address": "AA:01", "rssi": -60},
            ],
        },
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_locate_unknown_asset_returns_404(client):
    fp = await _setup_floor_with_aps(client)
    resp = await client.post(
        f"/api/v1/assets/{uuid4()}/locate",
        json={
            "floor_plan_id": fp["id"],
            "readings": [
                {"mac_address": "AA:00", "rssi": -40},
                {"mac_address": "AA:01", "rssi": -60},
                {"mac_address": "AA:02", "rssi": -60},
            ],
        },
    )
    assert resp.status_code == 404
