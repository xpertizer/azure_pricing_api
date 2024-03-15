from app.models.azure_price import AzurePrice
from app.models.product_details import ProductDetails
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base_class import Base
import pytest

DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_azure_price_product_detail_relationship(session):
    armSkuName = "Basic_A0"
    productName = "Virtual Machines A Series Basic"
    product_detail = ProductDetails(armSkuName=armSkuName, vCPUs=1, memory=0.75)
    session.add(product_detail)
    azure_price = AzurePrice(productName=productName, product_detail=product_detail, currencyCode="USD", ...)
    session.add(azure_price)
    session.commit()

    assert azure_price.product_detail == product_detail
    assert product_detail.azure_price == azure_price
