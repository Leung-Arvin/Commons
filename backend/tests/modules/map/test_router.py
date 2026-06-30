# backend/tests/modules/map/test_router.py
import pytest


@pytest.mark.asyncio
async def test_list_maps_empty(client):
    response = await client.get("/api/v1/maps/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_floor_plan_returns_spec_fields(client):
    payload = {
        "name": "HQ Floor 1",
        "building": "HQ",
        "floor": "1",
        "width": 50.0,
        "height": 30.0,
    }
    resp = await client.post("/api/v1/maps/", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "HQ Floor 1"
    assert body["building"] == "HQ"
    assert body["floor"] == "1"
    assert body["width"] == 50.0
    assert body["height"] == 30.0
    assert "id" in body
    # Detail response embeds children, empty on creation
    assert body["zones"] == []
    assert body["access_points"] == []


@pytest.mark.asyncio
async def test_list_floor_plans_returns_summaries(client):
    await client.post(
        "/api/v1/maps/",
        json={"name": "HQ Floor 2", "building": "HQ", "floor": "2", "width": 10, "height": 10},
    )
    resp = await client.get("/api/v1/maps/")
    assert resp.status_code == 200
    rows = resp.json()
    assert len(rows) == 1
    summary = rows[0]
    assert set(summary.keys()) == {"id", "name", "building", "floor"}
    assert summary["name"] == "HQ Floor 2"


@pytest.mark.asyncio
async def test_get_floor_plan_returns_detail(client):
    created = (
        await client.post(
            "/api/v1/maps/",
            json={
                "name": "HQ Floor 3",
                "building": "HQ",
                "floor": "3",
                "svg_url": "/static/hq-3.svg",
                "width": 20,
                "height": 15,
            },
        )
    ).json()
    resp = await client.get(f"/api/v1/maps/{created['id']}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == created["id"]
    assert body["svg_url"] == "/static/hq-3.svg"
    assert body["width"] == 20
    assert body["zones"] == []
    assert body["access_points"] == []


@pytest.mark.asyncio
async def test_get_floor_plan_not_found(client):
    resp = await client.get("/api/v1/maps/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


async def _create_map(client):
    return (
        await client.post(
            "/api/v1/maps/",
            json={"name": "Orig", "building": "B1", "floor": "1", "width": 10, "height": 10},
        )
    ).json()


@pytest.mark.asyncio
async def test_update_floor_plan_partial(client):
    created = await _create_map(client)
    resp = await client.put(
        f"/api/v1/maps/{created['id']}",
        json={"name": "Renamed", "floor": "5"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Renamed"
    assert body["floor"] == "5"
    assert body["building"] == "B1"  # untouched field preserved
    assert body["width"] == 10


@pytest.mark.asyncio
async def test_update_floor_plan_not_found(client):
    resp = await client.put(
        "/api/v1/maps/00000000-0000-0000-0000-000000000000",
        json={"name": "X"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_floor_plan(client):
    created = await _create_map(client)
    resp = await client.delete(f"/api/v1/maps/{created['id']}")
    assert resp.status_code == 204
    # gone afterwards
    assert (await client.get(f"/api/v1/maps/{created['id']}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_floor_plan_not_found(client):
    resp = await client.delete("/api/v1/maps/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
