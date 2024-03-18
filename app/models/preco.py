class Preco:
    def __init__(self, provedor, nomeMaquina, valor, cpu, disco, ram):
        self.provedor = provedor
        self.nomeMaquina = nomeMaquina
        self.valor = valor
        self.cpu = cpu
        self.disco = disco
        self.ram = ram

    def to_dict(self):
        """
        Converte a instância em um dicionário, que pode ser facilmente
        serializado em JSON.
        """
        return {
            "provedor": self.provedor,
            "nomeMaquina": self.nomeMaquina,
            "valor": self.valor,
            "cpu": self.cpu,
            "disco": self.disco,
            "ram": self.ram
        }