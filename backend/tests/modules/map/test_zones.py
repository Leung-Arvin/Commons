# backend/tests/modules/map/test_zones.py
import pytest


async def _create_map(client):
    resp = await client.post(
        "/api/v1/maps/",
        json={"name": "F", "building": "B", "floor": "1", "width": 10, "height": 10},
    )
    return resp.json()


@pytest.mark.asyncio
async def test_create_zone_returns_201_with_defaults(client):
    fp = await _create_map(client)
    payload = {"name": "Meeting Room A", "polygon": [[0, 0], [1, 0], [1, 1], [0, 1]]}
    resp = await client.post(f"/api/v1/maps/{fp['id']}/zones", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Meeting Room A"
    assert body["zone_type"] == "general"  # default applied
    assert body["polygon"] == [[0, 0], [1, 0], [1, 1], [0, 1]]
    assert body["floor_plan_id"] == fp["id"]
    assert "id" in body


@pytest.mark.asyncio
async def test_list_zones_for_map(client):
    fp = await _create_map(client)
    await client.post(
        f"/api/v1/maps/{fp['id']}/zones",
        json={"name": "Z1", "zone_type": "desk", "polygon": [[0, 0], [1, 1]]},
    )
    await client.post(
        f"/api/v1/maps/{fp['id']}/zones",
        json={"name": "Z2", "polygon": [[2, 2], [3, 3]]},
    )
    resp = await client.get(f"/api/v1/maps/{fp['id']}/zones")
    assert resp.status_code == 200
    zones = resp.json()
    assert len(zones) == 2
    assert {z["name"] for z in zones} == {"Z1", "Z2"}
    assert {z["zone_type"] for z in zones} == {"desk", "general"}


@pytest.mark.asyncio
async def test_zones_nested_in_floor_plan_detail(client):
    fp = await _create_map(client)
    await client.post(
        f"/api/v1/maps/{fp['id']}/zones",
        json={"name": "Z1", "polygon": [[0, 0], [1, 1]]},
    )
    resp = await client.get(f"/api/v1/maps/{fp['id']}")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["zones"]) == 1
    assert body["zones"][0]["name"] == "Z1"
    assert body["zones"][0]["floor_plan_id"] == fp["id"]


@pytest.mark.asyncio
async def test_create_zone_on_missing_map_returns_404(client):
    missing = "00000000-0000-0000-0000-000000000000"
    resp = await client.post(
        f"/api/v1/maps/{missing}/zones",
        json={"name": "Z1", "polygon": [[0, 0], [1, 1]]},
    )
    assert resp.status_code == 404
