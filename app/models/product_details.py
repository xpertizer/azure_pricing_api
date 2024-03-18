from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database.base_class import Base

class ProductDetails(Base):
    __tablename__ = "product_details"
    armSkuName = Column(String, primary_key=True, index=True)
    vCPUs = Column(Integer, nullable=False)
    memory = Column(Float, nullable=False)
    
    # A relação "azure_price" é definida aqui para conectar cada detalhe do produto a um preço específico do Azure.
    azure_price = relationship("AzurePrice", back_populates="product_detail", uselist=False)
