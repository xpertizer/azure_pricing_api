from sqlalchemy import Column, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base_class import Base

class AzurePrice(Base):
    __tablename__ = "azure_prices"
    meterId = Column(String, primary_key=True, index=True)
    currencyCode = Column(String, nullable=False)
    tierMinimumUnits = Column(Float, nullable=False)
    retailPrice = Column(String, nullable=False)
    unitPrice = Column(String, nullable=False)
    armRegionName = Column(String, nullable=False)
    location = Column(String, nullable=False)
    effectiveStartDate = Column(DateTime, nullable=False)
    productName = Column(String, ForeignKey('product_details.armSkuName'), nullable=False, unique=True)
    skuName = Column(String, nullable=False)
    serviceName = Column(String, nullable=False)
    serviceFamily = Column(String, nullable=False)
    unitOfMeasure = Column(String, nullable=False)
    type = Column(String, nullable=False)
    isPrimaryMeterRegion = Column(Boolean, nullable=False)
    armSkuName = Column(String, nullable=False)
    reservationTerm = Column(String, nullable=True)
    effectiveEndDate = Column(String, nullable=True)
    
    product_detail = relationship("ProductDetails", back_populates="azure_price", uselist=False)
