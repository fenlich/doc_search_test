from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app import service
from app.database import Base, engine, get_session
from app.schemas import DocumentOut
from app.search import ensure_index, es
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await ensure_index()
    await seed_if_empty()
    yield
    await es.close()
    await engine.dispose()


app = FastAPI(
    title="Documents Search Service",
    description="Полнотекстовый поиск по документам и удаление документов.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/search",
    response_model=list[DocumentOut],
    summary="Поиск документов по тексту",
    description="Ищет по тексту в индексе и возвращает первые 20 документов.",
)
async def search(
    q: str = Query(..., min_length=1, description="Текстовый запрос"),
    session: AsyncSession = Depends(get_session),
):
    return await service.search_documents(session, q)


@app.delete(
    "/documents/{doc_id}",
    status_code=204,
    summary="Удаление документа из БД и индекса",
    responses={404: {"description": "Документ не найден"}},
)
async def delete_document(doc_id: int, session: AsyncSession = Depends(get_session)):
    if not await service.delete_document(session, doc_id):
        raise HTTPException(status_code=404, detail="Документ не найден")
    return Response(status_code=204)

