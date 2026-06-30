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


async def _create_zone(client, map_id):
    resp = await client.post(
        f"/api/v1/maps/{map_id}/zones",
        json={"name": "Orig", "zone_type": "general", "polygon": [[0, 0], [1, 1]]},
    )
    return resp.json()


@pytest.mark.asyncio
async def test_update_zone_partial(client):
    fp = await _create_map(client)
    z = await _create_zone(client, fp["id"])
    resp = await client.put(
        f"/api/v1/maps/{fp['id']}/zones/{z['id']}",
        json={"name": "Renamed", "zone_type": "desk"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Renamed"
    assert body["zone_type"] == "desk"
    assert body["polygon"] == [[0, 0], [1, 1]]  # untouched field preserved
    assert body["floor_plan_id"] == fp["id"]


@pytest.mark.asyncio
async def test_update_zone_polygon(client):
    fp = await _create_map(client)
    z = await _create_zone(client, fp["id"])
    new_poly = [[0, 0], [2, 0], [2, 2], [0, 2]]
    resp = await client.put(
        f"/api/v1/maps/{fp['id']}/zones/{z['id']}",
        json={"polygon": new_poly},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["polygon"] == new_poly
    assert body["name"] == "Orig"  # untouched


@pytest.mark.asyncio
async def test_update_zone_not_found(client):
    fp = await _create_map(client)
    missing = "00000000-0000-0000-0000-000000000000"
    resp = await client.put(
        f"/api/v1/maps/{fp['id']}/zones/{missing}",
        json={"name": "X"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_zone_wrong_map_returns_404(client):
    fp1 = await _create_map(client)
    fp2 = await _create_map(client)
    z = await _create_zone(client, fp1["id"])
    # zone belongs to fp1; updating it via fp2's path must 404
    resp = await client.put(
        f"/api/v1/maps/{fp2['id']}/zones/{z['id']}",
        json={"name": "X"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_zone(client):
    fp = await _create_map(client)
    z = await _create_zone(client, fp["id"])
    resp = await client.delete(f"/api/v1/maps/{fp['id']}/zones/{z['id']}")
    assert resp.status_code == 204
    # gone afterwards
    zones = (await client.get(f"/api/v1/maps/{fp['id']}/zones")).json()
    assert zones == []


@pytest.mark.asyncio
async def test_delete_zone_not_found(client):
    fp = await _create_map(client)
    missing = "00000000-0000-0000-0000-000000000000"
    resp = await client.delete(f"/api/v1/maps/{fp['id']}/zones/{missing}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_zone_wrong_map_returns_404(client):
    fp1 = await _create_map(client)
    fp2 = await _create_map(client)
    z = await _create_zone(client, fp1["id"])
    resp = await client.delete(f"/api/v1/maps/{fp2['id']}/zones/{z['id']}")
    assert resp.status_code == 404
    # still present under its real map
    zones = (await client.get(f"/api/v1/maps/{fp1['id']}/zones")).json()
    assert len(zones) == 1
