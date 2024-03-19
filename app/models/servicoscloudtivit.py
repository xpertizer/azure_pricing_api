from sqlalchemy import Column, Float, Integer, String
# Importando Base do local especificado no seu projeto
from ..database.base_class import Base

class ServicosCloudTivit(Base):
    __tablename__ = "preco_servicos_cloud"
    # Definindo a estrutura da tabela conforme os requisitos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    PN_Interno = Column(String(255), nullable=False)
    Desc_Item = Column(String(255), nullable=False)
    On_Demand = Column(Float, nullable=False)
    Ano_1 = Column(Float, nullable=False)
    Ano_2 = Column(Float, nullable=False)
    Ano_3 = Column(Float, nullable=False)
    Ano_4 = Column(Float, nullable=False)
    Ano_5 = Column(Float, nullable=False)