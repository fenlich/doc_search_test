from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.models import Document
from app.search import delete_from_index, index_documents, search_ids


async def create_documents(session: AsyncSession, docs: list[Document]) -> list[Document]:
    session.add_all(docs)
    await session.commit()     
    await index_documents(docs)
    return docs


async def search_documents(session: AsyncSession, query: str) -> list[Document]:
    ids = await search_ids(query)
    if not ids:
        return []
    stmt = (
        select(Document)
        .where(Document.id.in_(ids))
        .limit(settings.search_limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def delete_document(session: AsyncSession, doc_id: int) -> bool:
    doc = await session.get(Document, doc_id)
    if doc is None:
        return False
    await session.delete(doc)
    await session.commit()
    await delete_from_index(doc_id)
    return True