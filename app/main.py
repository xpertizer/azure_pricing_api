from fastapi import FastAPI
from app.api.routes import imports, tivit_prices, consolidate_prices, azure_prices, gcp_prices, aws_prices
from .database.session import engine
from .models import azure_price, product_details, servicoscloudtivit

app = FastAPI()

azure_price.Base.metadata.create_all(bind=engine)
product_details.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Azure Pricing API")

app.include_router(azure_prices.router, prefix="/azure-pricing", tags=["Azure Pricing"])
app.include_router(imports.router, prefix="/importacoes", tags=["Imports"])
app.include_router(tivit_prices.router, prefix="/tivit-pricing", tags=["Tivit Pricing"])
app.include_router(aws_prices.router, prefix="/aws-pricing", tags=["AWS Pricing"])
app.include_router(gcp_prices.router, prefix="/gcp-pricing", tags=["GCP Pricing"])
app.include_router(consolidate_prices.router, prefix="/consolidate-pricing", tags=["Consolidate Pricing"])
