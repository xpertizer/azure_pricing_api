from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import SessionLocal
from app.models.servicoscloudtivit import ServicosCloudTivit

router = APIRouter()

@router.get('/filtered-prices')
async def get_itemVcloudModel(page: int = 1, limit: int = 10, db: AsyncSession = Depends(SessionLocal)):
    async with db as session:
        # Realiza a consulta com paginação
        query = select(ServicosCloudTivit).offset((page - 1) * limit).limit(limit)
        result = await session.execute(query)
        items = result.scalars().all()
        return {"data": [item.__dict__ for item in items], "count": len(items)}