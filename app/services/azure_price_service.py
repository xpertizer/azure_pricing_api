from ..database.session import SessionLocal
from ..models.azure_price import AzurePrice
from ..models.product_details import ProductDetails
import requests
import csv
from fastapi import UploadFile

def fetch_and_update_azure_prices():
    db = SessionLocal()
    try:
        response = requests.get("https://api.example.com/azure-prices")
        prices = response.json()
        for price_data in prices:
            product_detail = db.query(ProductDetails).filter_by(armSkuName=price_data["productName"]).first()
            if not product_detail:
                product_detail = ProductDetails(armSkuName=price_data["productName"])
                db.add(product_detail)
            azure_price = db.query(AzurePrice).filter_by(productName=price_data["productName"]).first()
            if not azure_price:
                azure_price = AzurePrice(productName=price_data["productName"], product_detail=product_detail, currencyCode="USD", retailPrice=price_data["retailPrice"], unitPrice=price_data["unitPrice"])
                db.add(azure_price)
        db.commit()
    finally:
        db.close()

def get_azure_prices():
    db = SessionLocal()
    try:
        return db.query(AzurePrice).all()
    finally:
        db.close()
async def load_product_details_from_csv(file: UploadFile):
    db = SessionLocal()
    try:
        contents = await file.read()
        csv_reader = csv.DictReader(contents.decode().splitlines(), delimiter=';')
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
    finally:
        db.close()
