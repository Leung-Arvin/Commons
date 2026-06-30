# backend/tests/modules/map/test_access_points.py
import pytest


async def _create_map(client):
    resp = await client.post(
        "/api/v1/maps/",
        json={"name": "F", "building": "B", "floor": "1", "width": 10, "height": 10},
    )
    return resp.json()


@pytest.mark.asyncio
async def test_create_access_point_returns_201(client):
    fp = await _create_map(client)
    payload = {"mac_address": "aa:bb:cc:dd:ee:01", "name": "AP-1", "x": 5.0, "y": 7.5}
    resp = await client.post(f"/api/v1/maps/{fp['id']}/aps", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["mac_address"] == "aa:bb:cc:dd:ee:01"
    assert body["name"] == "AP-1"
    assert body["x"] == 5.0
    assert body["y"] == 7.5
    assert body["floor_plan_id"] == fp["id"]
    assert "id" in body


@pytest.mark.asyncio
async def test_create_access_point_name_optional(client):
    fp = await _create_map(client)
    resp = await client.post(
        f"/api/v1/maps/{fp['id']}/aps",
        json={"mac_address": "aa:bb:cc:dd:ee:02", "x": 1.0, "y": 2.0},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] is None


@pytest.mark.asyncio
async def test_list_access_points_for_map(client):
    fp = await _create_map(client)
    await client.post(
        f"/api/v1/maps/{fp['id']}/aps",
        json={"mac_address": "aa:bb:cc:dd:ee:03", "x": 1, "y": 1},
    )
    await client.post(
        f"/api/v1/maps/{fp['id']}/aps",
        json={"mac_address": "aa:bb:cc:dd:ee:04", "x": 2, "y": 2},
    )
    resp = await client.get(f"/api/v1/maps/{fp['id']}/aps")
    assert resp.status_code == 200
    aps = resp.json()
    assert len(aps) == 2
    assert {a["mac_address"] for a in aps} == {"aa:bb:cc:dd:ee:03", "aa:bb:cc:dd:ee:04"}


@pytest.mark.asyncio
async def test_access_points_nested_in_floor_plan_detail(client):
    fp = await _create_map(client)
    await client.post(
        f"/api/v1/maps/{fp['id']}/aps",
        json={"mac_address": "aa:bb:cc:dd:ee:05", "x": 3, "y": 4},
    )
    resp = await client.get(f"/api/v1/maps/{fp['id']}")
    body = resp.json()
    assert len(body["access_points"]) == 1
    assert body["access_points"][0]["mac_address"] == "aa:bb:cc:dd:ee:05"
    assert body["access_points"][0]["floor_plan_id"] == fp["id"]


@pytest.mark.asyncio
async def test_create_access_point_on_missing_map_returns_404(client):
    missing = "00000000-0000-0000-0000-000000000000"
    resp = await client.post(
        f"/api/v1/maps/{missing}/aps",
        json={"mac_address": "aa:bb:cc:dd:ee:06", "x": 1, "y": 1},
    )
    assert resp.status_code == 404
