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


async def _create_ap(client, map_id):
    resp = await client.post(
        f"/api/v1/maps/{map_id}/aps",
        json={"mac_address": "aa:bb:cc:dd:ee:10", "name": "Orig", "x": 1.0, "y": 2.0},
    )
    return resp.json()


@pytest.mark.asyncio
async def test_update_access_point_partial(client):
    fp = await _create_map(client)
    ap = await _create_ap(client, fp["id"])
    resp = await client.put(
        f"/api/v1/maps/{fp['id']}/aps/{ap['id']}",
        json={"name": "AP-Renamed", "x": 9.0, "y": 8.0},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "AP-Renamed"
    assert body["x"] == 9.0
    assert body["y"] == 8.0
    assert body["mac_address"] == "aa:bb:cc:dd:ee:10"  # untouched field preserved
    assert body["floor_plan_id"] == fp["id"]


@pytest.mark.asyncio
async def test_update_access_point_mac(client):
    fp = await _create_map(client)
    ap = await _create_ap(client, fp["id"])
    resp = await client.put(
        f"/api/v1/maps/{fp['id']}/aps/{ap['id']}",
        json={"mac_address": "aa:bb:cc:dd:ee:ff"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["mac_address"] == "aa:bb:cc:dd:ee:ff"
    assert body["name"] == "Orig"  # untouched
    assert body["x"] == 1.0


@pytest.mark.asyncio
async def test_update_access_point_not_found(client):
    fp = await _create_map(client)
    missing = "00000000-0000-0000-0000-000000000000"
    resp = await client.put(
        f"/api/v1/maps/{fp['id']}/aps/{missing}",
        json={"name": "X"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_access_point_wrong_map_returns_404(client):
    fp1 = await _create_map(client)
    fp2 = await _create_map(client)
    ap = await _create_ap(client, fp1["id"])
    resp = await client.put(
        f"/api/v1/maps/{fp2['id']}/aps/{ap['id']}",
        json={"name": "X"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_access_point(client):
    fp = await _create_map(client)
    ap = await _create_ap(client, fp["id"])
    resp = await client.delete(f"/api/v1/maps/{fp['id']}/aps/{ap['id']}")
    assert resp.status_code == 204
    aps = (await client.get(f"/api/v1/maps/{fp['id']}/aps")).json()
    assert aps == []


@pytest.mark.asyncio
async def test_delete_access_point_not_found(client):
    fp = await _create_map(client)
    missing = "00000000-0000-0000-0000-000000000000"
    resp = await client.delete(f"/api/v1/maps/{fp['id']}/aps/{missing}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_access_point_wrong_map_returns_404(client):
    fp1 = await _create_map(client)
    fp2 = await _create_map(client)
    ap = await _create_ap(client, fp1["id"])
    resp = await client.delete(f"/api/v1/maps/{fp2['id']}/aps/{ap['id']}")
    assert resp.status_code == 404
    aps = (await client.get(f"/api/v1/maps/{fp1['id']}/aps")).json()
    assert len(aps) == 1
