from fastapi import APIRouter, HTTPException, UploadFile, File
from ...services.azure_price_service import fetch_and_update_azure_prices, get_azure_prices, load_product_details_from_csv


router = APIRouter()

@router.get("/atualizar-precos")
def atualizar_precos():
    try:
        fetch_and_update_azure_prices()
        return {"message": "Preços atualizados com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/carga-produtos")
async def carga_produtos(file: UploadFile = File(...)):
    try:
        await load_product_details_from_csv(file)
        return {"message": "Detalhes dos produtos carregados com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/listar-precos")
def listar_precos():
    try:
        prices = get_azure_prices()
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
