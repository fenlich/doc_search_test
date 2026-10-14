import os
import httpx
import pytest


BASE_URL = os.getenv("API_URL", "http://localhost:8000")

@pytest.mark.asyncio
async def test_search_returns_documents():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/search", params={"q": "девушки"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 20

    if data:
        doc = data[0]
        assert {"id", "rubrics", "text", "created_date"} <= set(doc.keys())


@pytest.mark.asyncio
async def test_delete_missing_document():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete("/documents/999999999")

    assert response.status_code == 404