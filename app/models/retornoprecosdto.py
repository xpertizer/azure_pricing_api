class RetornoPrecosDTO:
    def __init__(self, precos):
        self.precos = precos
        self.quantidade = len(precos)

    def to_dict(self):
        """
        Converte a instância em um dicionário, incluindo a conversão
        da lista de Preco em uma lista de dicionários.
        """
        return {
            "precos": [preco.to_dict() for preco in self.precos],
            "quantidade": self.quantidade
        }