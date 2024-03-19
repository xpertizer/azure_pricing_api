from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from ...services.azure_price_service import fetch_and_update_azure_prices, get_azure_prices, load_product_details_from_csv, criar_retorno_precos_dto

router = APIRouter()

@router.get("/RefreshPricesFromAzureRetailPricesApi")
def atualizar_precos():
    try:
        fetch_and_update_azure_prices()
        return {"message": "Prices Updated Successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/OriginalAzurePriceList")
def listar_precos():
    try:
        prices = get_azure_prices()
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/filtered-prices")
def filtrar_precos(cpu: int = Query(None), ram: float = Query(None), disco: str = Query(None)):
    try:
        # Chamada à função criar_retorno_precos_dto com os filtros recebidos
        # Note que o filtro_disco não será aplicado, pois os dados não contêm informações sobre disco.
        # O parâmetro disco é mantido para demonstrar como receberia e passaria esse parâmetro se fosse aplicável.
        retorno_precos_dto = criar_retorno_precos_dto(filtro_cpu=cpu, filtro_ram=ram, filtro_disco=disco)
        
        # Convertendo o objeto RetornoPrecosDTO para dicionário para facilitar a resposta JSON
        resposta = retorno_precos_dto.to_dict()
        
        return resposta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))