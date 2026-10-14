from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from app.config import settings

es = AsyncElasticsearch(settings.elasticsearch_url)


MAPPING = {
    "properties": {
        "id": {"type": "integer"},
        "text": {"type": "text", "analyzer": "russian"},
    }
}


async def ensure_index() -> None:
    if not await es.indices.exists(index=settings.es_index):
        await es.indices.create(index=settings.es_index, mappings=MAPPING)


async def count_indexed() -> int:
    resp = await es.count(index=settings.es_index)
    return resp["count"]


async def index_documents(docs) -> None:
    actions = (
        {
            "_index": settings.es_index,
            "_id": d.id,
            "_source": {"id": d.id, "text": d.text},
        }
        for d in docs
    )
    await async_bulk(es, actions, refresh=True)


async def search_ids(query: str) -> list[int]:
    resp = await es.search(
        index=settings.es_index,
        query={"match": {"text": query}},
        size=10_000,
        source=False,
    )
    return [int(hit["_id"]) for hit in resp["hits"]["hits"]]


async def delete_from_index(doc_id: int) -> None:
    await es.options(ignore_status=404).delete(
        index=settings.es_index, id=str(doc_id), refresh=True
    )