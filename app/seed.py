import ast
import csv
from datetime import datetime
from pathlib import Path
from sqlalchemy import func, select
from app.config import settings
from app.database import SessionLocal
from app.models import Document
from app.search import count_indexed, index_documents
from app.service import create_documents


async def seed_if_empty() -> None:
    async with SessionLocal() as session:
        total = await session.scalar(select(func.count()).select_from(Document))

        if total == 0:
            path = Path(settings.seed_csv_path)
            if not path.exists():
                return
            with path.open(encoding="utf-8", newline="") as f:
                docs = [
                    Document(
                        text=row["text"],
                        created_date=datetime.strptime(row["created_date"], "%Y-%m-%d %H:%M:%S"),
                        rubrics=ast.literal_eval(row["rubrics"]),
                    )
                    for row in csv.DictReader(f)
                ]
            await create_documents(session, docs)
            return

        if await count_indexed() == 0:
            docs = (await session.execute(select(Document))).scalars().all()
            await index_documents(docs)