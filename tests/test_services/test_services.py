# Exemplo de teste para o serviço azure_price_service
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import azure_price_service

class TestAzurePriceService(unittest.TestCase):
    
    class TestAzurePriceService(unittest.TestCase):
        @patch('azure_price_service.pd.read_csv')
        def test_load_product_details_from_csv(self, mock_read_csv):
            # Mock dos dados retornados pela função read_csv
            mock_read_csv.return_value = pd.DataFrame({
                'armSkuName': ['SKU1', 'SKU2', 'SKU3'],
                'vCPUs': [2, 4, 6],
                'memory': [4, 8, 16]
            })

            # Chama a função
            result = azure_price_service.load_product_details_from_csv('fake_path')

            # Verifica se a função foi chamada com os parâmetros corretos
            mock_read_csv.assert_called_once_with('fake_path')

            # Verifica se o resultado é o esperado
            self.assertEqual(len(result), 3)
            self.assertEqual(result['SKU1'].vCPUs, 2)
            self.assertEqual(result['SKU1'].memory, 4)
            self.assertEqual(result['SKU2'].vCPUs, 4)
            self.assertEqual(result['SKU2'].memory, 8)
            self.assertEqual(result['SKU3'].vCPUs, 6)
            self.assertEqual(result['SKU3'].memory, 16)
        
        @patch('azure_price_service.requests.get')
        @patch('azure_price_service.SessionLocal')
        def test_fetch_and_update_azure_prices(self, mock_SessionLocal, mock_get):
            # Mock dos dados retornados pela função get
            mock_get.return_value.json.return_value = {
                'Items': [
                    {
                        "armSkuName": "SKU1",
                        "meterId": "123",
                        "currencyCode": "BRL",
                        "effectiveStartDate": "2022-01-01T00:00:00Z"
                    },
                    {
                        "armSkuName": "SKU2",
                        "meterId": "456",
                        "currencyCode": "BRL",
                        "effectiveStartDate": "2022-01-01T00:00:00Z"
                    }
                ]
            }

            # Mock do objeto de sessão do banco de dados
            mock_db = MagicMock()
            mock_SessionLocal.return_value = mock_db

            # Chama a função
            azure_price_service.fetch_and_update_azure_prices()

            # Verifica se as funções foram chamadas com os parâmetros corretos
            mock_get.assert_called_once()
            mock_db.query.assert_called()

        @patch('azure_price_service.get_azure_prices')
        def test_criar_retorno_precos_dto(self, mock_get_azure_prices):
            # Mock dos dados retornados pela função get_azure_prices
            mock_get_azure_prices.return_value = [
                MagicMock(armSkuName='SKU1', retailPrice=100, product_detail=MagicMock(vCPUs=2, memory=4)),
                MagicMock(armSkuName='SKU2', retailPrice=200, product_detail=MagicMock(vCPUs=4, memory=8)),
                MagicMock(armSkuName='SKU3', retailPrice=300, product_detail=MagicMock(vCPUs=6, memory=16)),
            ]

            # Teste sem filtros
            result = azure_price_service.criar_retorno_precos_dto()
            self.assertEqual(len(result.precos), 3)

            # Teste com filtro de CPU
            result = azure_price_service.criar_retorno_precos_dto(filtro_cpu=4)
            self.assertEqual(len(result.precos), 1)
            self.assertEqual(result.precos[0].cpu, 4)

            # Teste com filtro de RAM
            result = azure_price_service.criar_retorno_precos_dto(filtro_ram=16)
            self.assertEqual(len(result.precos), 1)
            self.assertEqual(result.precos[0].ram, 16)

    if __name__ == '__main__':
        unittest.main()