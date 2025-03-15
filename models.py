class Produto:
    def __init__(self, id, nome, tipo, validade, quantidade, preco_compra, preco_venda):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.validade = validade
        self.quantidade = quantidade
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda

class Venda:
    def __init__(self, id, produto_id, quantidade, data, hora, total):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.data = data
        self.hora = hora
        self.total = total