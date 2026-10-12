from dataclasses import dataclass
from contextlib import contextmanager

class EstoqueError(Exception):
    pass

class ProdutoNaoEncontradoError(EstoqueError):

    def __init__(self, codigo):
        super().__init__(f"Produto: {codigo} não encontrado")
        self.codigo = codigo


class EstoqueInsuficienteError(EstoqueError):

    def __init__(self, codigo, disponivel, solicitado):
        super().__init__("Saldo insuficiente")
        self.codigo = codigo
        self.disponivel = disponivel
        self.solicitado = solicitado

class QuantidadeInvalidaError(EstoqueError):

    def __init__(self, quantidade):
        super().__init__("Quantidade inválida")
        self.quantidade = quantidade

class PedidoRecusadoError(EstoqueError):

    def __init__(self, indice):
        super().__init__("Produto recusado")
        self.indice = indice

@dataclass( frozen=True)
class Produto:
    codigo: str
    nome: str
    preco: float

    def __post_init__(self):
        if self.preco <= 0:
            raise ValueError("Preço não pode ser zero ou negativo") 


class Estoque:

    def __init__(self):
        self.produtos = {}
        self.quantidades ={}

    @property
    def valor_total(self) -> float:
        return sum(self.quantidades[chave] * produto.preco for chave, produto in self.produtos.items())
 
    def adicionar(self, produto: Produto, quantidade: int):

        if quantidade <= 0:
            raise QuantidadeInvalidaError(quantidade)        

        if  produto.codigo not in self.produtos:
            self.produtos[produto.codigo] = produto
            self.quantidades[produto.codigo] = quantidade
        else:
            self.quantidades[produto.codigo] = self.quantidades.get(produto.codigo, 0) + quantidade

    def remover(self,codigo: str, quantidade: int):      
        
        if quantidade <= 0:
            raise QuantidadeInvalidaError(quantidade)        
 
        if codigo not in self.produtos:
            raise ProdutoNaoEncontradoError(codigo)

        quantidade_apos_remocao = self.quantidades.get(codigo, 0) - quantidade

        if quantidade_apos_remocao < 0:
            raise EstoqueInsuficienteError(codigo,self.quantidades.get(codigo, 0), quantidade)    

        self.quantidades[codigo] = quantidade_apos_remocao

    def quantidade(self, codigo: str) -> int:

        if codigo not in self.produtos:
            raise ProdutoNaoEncontradoError(codigo) 
        
        return self.quantidades.get(codigo, 0)    

    def __contains__(self, codigo: str) -> bool:        
        return codigo in self.produtos 

    @contextmanager
    def transacao(self):
        backup_quantidades = self.quantidades.copy()
        try:
            yield
        except:
            self.quantidades = backup_quantidades
            raise



def processar_pedido(estoque: Estoque, itens: list[tuple[str, int]]):
    pass
        
#testes manuais
if __name__ == "__main__":
    estoque1 = Estoque()

    estoque1.adicionar(Produto("PR1","PRODUTO1",10),32)
    estoque1.adicionar(Produto("PR1","PRODUTO1",10),12)
    estoque1.adicionar(Produto("PR2","PRODUTO2",6),5)

    print(estoque1.valor_total)

    print("PR2" in estoque1)    
    print("PR3" in estoque1)    

    estoque1.remover("PR2",2)

    print(estoque1.quantidades.get("PR2"))

    try:
        estoque1.remover("PR2",-2)  
    except QuantidadeInvalidaError as e:
        print(e)

    try:
        estoque1.remover("PR10",2)  
    except ProdutoNaoEncontradoError as e:
        print(e)

    try:
        estoque1.remover("PR2",10)  
    except EstoqueInsuficienteError as e:
        print(e)

    print(estoque1.quantidades)
    try:
        with estoque1.transacao():
            estoque1.remover("PR1", 5)  
            estoque1.remover("PR2", 999)  
    except EstoqueInsuficienteError as e:
        print("Erro:", e)
    print(estoque1.quantidades)









    