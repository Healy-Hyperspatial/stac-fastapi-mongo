import pytest

# - BASIC_AUTH={"public_endpoints":[{"path":"/","method":"GET"},{"path":"/search","method":"GET"}],"users":[{"username":"admin","password":"admin","permissions":"*"},{"username":"reader","password":"reader","permissions":[{"path":"/conformance","method":["GET"]},{"path":"/collections/{collection_id}/items/{item_id}","method":["GET"]},{"path":"/search","method":["POST"]},{"path":"/collections","method":["GET"]},{"path":"/collections/{collection_id}","method":["GET"]},{"path":"/collections/{collection_id}/items","method":["GET"]},{"path":"/queryables","method":["GET"]},{"path":"/queryables/collections/{collection_id}/queryables","method":["GET"]},{"path":"/_mgmt/ping","method":["GET"]}]}]}


@pytest.mark.asyncio
async def test_get_search_not_authenticated(app_client_basic_auth):
    """Test public endpoint search without authentication"""
    params = {"query": '{"gsd": {"gt": 14}}'}

    response = await app_client_basic_auth.get("/search", params=params)

    assert response.status_code == 200
    assert response.json() == {
        "type": "FeatureCollection",
        "features": [],
        "links": [],
        "context": {"returned": 0, "limit": 10, "matched": 0},
    }


@pytest.mark.asyncio
async def test_post_search_authenticated(app_client_basic_auth):
    """Test protected post search with reader auhtentication"""
    params = {
        "bbox": [97.504892, -45.254738, 174.321298, -2.431580],
        "fields": {"exclude": ["properties"]},
    }
    headers = {"Authorization": "Basic cmVhZGVyOnJlYWRlcg=="}

    response = await app_client_basic_auth.post("/search", json=params, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "type": "FeatureCollection",
        "features": [],
        "links": [],
        "context": {"returned": 0, "limit": 10, "matched": 0},
    }


@pytest.mark.asyncio
async def test_delete_resource_insufficient_permissions(app_client_basic_auth):
    """Test protected delete collection with reader auhtentication"""
    headers = {
        "Authorization": "Basic cmVhZGVyOnJlYWRlcg=="
    }  # Assuming this is a valid authorization token

    response = await app_client_basic_auth.delete(
        "/collections/test-collection", headers=headers
    )

    assert (
        response.status_code == 403
    )  # Expecting a 403 status code for insufficient permissions
    assert response.json() == {
        "detail": "Insufficient permissions for [DELETE /collections/test-collection]"
    }
