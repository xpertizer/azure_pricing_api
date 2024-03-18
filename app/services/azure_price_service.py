from datetime import datetime
from ..database.session import SessionLocal
from ..models.azure_price import AzurePrice
from ..models.product_details import ProductDetails
from ..models.azure_price import AzurePrice
import requests
import csv
from fastapi import UploadFile
from sqlalchemy.orm import joinedload

def fetch_and_update_azure_prices():
    db = SessionLocal()
    try:
        # URL inicial
        currency = 'BRL'
        url = f"https://prices.azure.com/api/retail/prices?currencyCode=%27{currency}%27&$filter=serviceFamily%20eq%20%27Compute%27%20and%20armRegionName%20eq%20%27brazilsouth%27%20or%20armRegionName%20eq%20%27brazilsouthest%27"

        response = requests.get(url)
        prices = response.json()['Items']
        for price_data in prices:
            # product_detail = db.query(ProductDetails).filter_by(armSkuName=price_data["armSkuName"]).first()
            # if not product_detail:
            #     product_detail = ProductDetails(armSkuName=price_data["armSkuName"])
            #     db.add(product_detail)
            
            azure_price =  db.query(AzurePrice).filter_by(armSkuName=price_data["armSkuName"]).first()
            if not azure_price:
                effective_start_date = datetime.strptime(price_data["effectiveStartDate"], "%Y-%m-%dT%H:%M:%SZ")
                azure_price = AzurePrice(
                    meterId=price_data["meterId"],
                    currencyCode=price_data["currencyCode"],
                    tierMinimumUnits=price_data["tierMinimumUnits"],
                    retailPrice=price_data["retailPrice"],
                    unitPrice=price_data["unitPrice"],
                    armRegionName=price_data["armRegionName"],
                    location=price_data["location"],
                    effectiveStartDate=effective_start_date,
                    productName=price_data["productName"],
                    skuName=price_data["skuName"],
                    serviceName=price_data["serviceName"],
                    serviceFamily=price_data["serviceFamily"],
                    unitOfMeasure=price_data["unitOfMeasure"],
                    type=price_data["type"],
                    isPrimaryMeterRegion=price_data["isPrimaryMeterRegion"],
                    armSkuName=price_data["armSkuName"],
                    #product_detail=product_detail
                )
                db.add(azure_price)
            
        db.commit()
    finally:
        db.close()

# def get_azure_prices():
#     db = SessionLocal()
#     try:
#         return db.query(AzurePrice).all()
#     finally:
#         db.close()
def get_azure_prices():
    db = SessionLocal()
    try:
        # Modifica a consulta para incluir um joinedload de 'product_detail'.
        # Isso garante que os detalhes do produto sejam carregados na mesma consulta dos preços do Azure.
        azure_prices_with_details = db.query(AzurePrice).options(joinedload(AzurePrice.product_detail)).all()
        return azure_prices_with_details
    finally:
        db.close()
        
async def load_product_details_from_csv(file: UploadFile):
    db = SessionLocal()
    try:
        contents = await file.read()
        csv_reader = csv.DictReader(contents.decode('utf-8-sig').splitlines(), delimiter=';')
        for row in csv_reader:
            product_detail = db.query(ProductDetails).filter_by(armSkuName=row['VM Name']).first()
            if not product_detail:
                product_detail = ProductDetails(
                    armSkuName=row['VM Name'],
                    vCPUs=int(row['vCPUs']),
                    memory=float(row['Memory (GiB)'])
                )
                db.add(product_detail)
        db.commit()
    except Exception as e:
        print(e.message)
        db.rollback()
        #raise e
    finally:
        db.close()
