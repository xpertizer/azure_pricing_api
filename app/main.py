from fastapi import FastAPI
from .database.session import engine
from .models import azure_price, product_details
from .api.routes import azure_prices

app = FastAPI()

azure_price.Base.metadata.create_all(bind=engine)
product_details.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Azure Pricing API")

app.include_router(azure_prices.router, prefix="/azure-pricing", tags=["Azure Pricing"])
