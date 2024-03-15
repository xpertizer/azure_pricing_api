# Azure Pricing API

Este projeto é uma API construída com FastAPI para interagir com preços da Azure e detalhes de produtos, utilizando SQLAlchemy para o ORM e pytest para testes unitários.

## Configuração do Ambiente

Para rodar este projeto, é recomendado criar um ambiente virtual Python e instalar as dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # Para Windows use 'venv\Scripts\activate'
pip install -r requirements.txt
```

## Executando a Aplicação

Para iniciar a aplicação, utilize o seguinte comando:

```bash
uvicorn app.main:app --reload
```

Isso iniciará o servidor de desenvolvimento FastAPI na porta 8000, e a API estará disponível em: http://localhost:8000

## Testes

Para rodar os testes unitários, execute:

```bash
pytest
```

## Migrações

Para criar e aplicar migrações do banco de dados, use Alembic:

```bash
alembic revision --autogenerate -m "Descrição da mudança"
alembic upgrade head
```

Assegure-se de ajustar as configurações de conexão com o banco de dados conforme necessário.

## Endpoints

A API possui os seguintes endpoints:

- POST /azure-pricing/carga-produtos: Carrega detalhes dos produtos via arquivo CSV.
- GET /azure-pricing/atualizar-precos: Atualiza os preços a partir da API da Azure.
- GET /azure-pricing/listar-precos: Lista os preços e detalhes dos produtos.

Consulte a documentação da API gerada pelo FastAPI para mais detalhes: http://localhost:8000/docs
