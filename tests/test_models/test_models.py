from app.models.azure_price import AzurePrice
from app.models.product_details import ProductDetails
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base_class import Base
import pytest

DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestDatabaseModels:
    @pytest.fixture(scope="function")
    def session(self):
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
        db.close()
        Base.metadata.drop_all(bind=engine)

    def test_azure_price_product_detail_relationship(self, session):
        armSkuName = "Basic_A0"
        productName = "Virtual Machines A Series Basic"
        product_detail = ProductDetails(armSkuName=armSkuName, vCPUs=1, memory=0.75)
        session.add(product_detail)
        azure_price = AzurePrice(productName=productName, product_detail=product_detail, currencyCode="USD", retailPrice=0.0, armSkuName=armSkuName, meterId="123", tierMinimumUnits=0, unitPrice=0.0, armRegionName="brazilsouth", location="brazilsouth", effectiveStartDate="2022-01-01T00:00:00Z", skuName="Basic_A0", serviceName="Virtual Machines", serviceFamily="Compute", unitOfMeasure="1 Hour", type="DevTestConsumption", isPrimaryMeterRegion=True)
        session.add(azure_price)
        session.commit()

        assert azure_price.product_detail == product_detail
        assert product_detail.azure_price == azure_price
