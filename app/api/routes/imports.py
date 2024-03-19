from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict
from app.database.session import SessionLocal
from app.models.servicoscloudtivit import ServicosCloudTivit
import pandas as pd

router = APIRouter()

async def read_excel_to_df(file: UploadFile) -> pd.DataFrame:
    """Lê um arquivo Excel e o converte em um DataFrame do pandas."""
    return pd.read_excel(BytesIO(await file.read()), engine="openpyxl", sheet_name="EC VM Preco VDC", skiprows=6, usecols="A:I")

def rename_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia as colunas do DataFrame para manter a consistência."""
    return df.rename(columns={
        "PN Interno": "PN_Interno",
        "Desc Item": "Desc_Item",
        "On Demand": "On_Demand",
        "1 ano": "Ano_1",
        "2 anos": "Ano_2",
        "3 anos": "Ano_3",
        "4 anos": "Ano_4",
        "5 anos": "Ano_5"
    })

@router.post('/LoadTivitData')  
async def importardadostivit(file: UploadFile = File(...), db: AsyncSession = Depends(SessionLocal)):
    try:
        df = await read_excel_to_df(file)
        df = rename_df_columns(df)

        async with db as session:
            # Limpa a tabela antes de inserir novos dados
            await session.execute(delete(ServicosCloudTivit))
            await session.commit()

            # Insere os novos dados na tabela
            for _, row in df.iterrows():
                if not pd.isna(row['PN_Interno']):
                    session.add(ServicosCloudTivit(**row.to_dict()))
            await session.commit()

        return {"message": "Dados inseridos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/LoadAzureProductsDetails")
async def carga_produtos(file: UploadFile = File(...)):
    db = SessionLocal()
    try:
        df = await read_excel_to_df(file)
        df = rename_df_columns(df)

        async with db as session:
            # Limpa a tabela antes de inserir novos dados
            await session.execute(delete(ServicosCloudTivit))
            await session.commit()

            # Insere os novos dados na tabela
            for _, row in df.iterrows():
                if not pd.isna(row['PN_Interno']):
                    session.add(ServicosCloudTivit(**row.to_dict()))
            await session.commit()

        return {"message": "Dados inseridos com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))