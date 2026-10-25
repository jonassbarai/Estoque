import pytest
from estoque import Estoque, EstoqueError, EstoqueInsuficienteError, PedidoRecusadoError, Produto, ProdutoNaoEncontradoError, QuantidadeInvalidaError, processar_pedido


@pytest.mark.parametrize("codigo, nome, preco",
    [
        ("PR1", "Produto1", -1),
        ("PR2", "Produto2", -10),
        ("PR2", "Produto2", 0)
    ]    
)
def test_produto_preco_Invalido(codigo, nome, preco):
    with pytest.raises(ValueError):
        Produto(codigo, nome,preco)


def test_adicionar_produto(estoque_vazio: Estoque):
    produto = Produto("PR1-TESTE","PRODUTO TESTE", 15.69)
    estoque_vazio.adicionar(produto, 10)
    estoque_vazio.adicionar(produto, 10)

    assert estoque_vazio.quantidades == {"PR1-TESTE": 20}
    assert estoque_vazio.produtos == {'PR1-TESTE': Produto(codigo='PR1-TESTE', nome='PRODUTO TESTE', preco=15.69)}


def test_adicionar_produto_quantidade_invalida(estoque_vazio): 
    with pytest.raises(QuantidadeInvalidaError) as exc_info:
        estoque_vazio.adicionar(Produto("PR1-TESTE","PRODUTO TESTE", 15.69), 0)

    assert exc_info.value.quantidade == 0

def test_remover_produto(estoque: Estoque):
    estoque.remover("PR1", 10)
    assert  estoque.quantidades == {"PR1": 20, "PR2": 5}

def test_remover_produto_qtd_invalida(estoque: Estoque):
    with pytest.raises(QuantidadeInvalidaError) as exc_info:
        estoque.remover("PR1", -10)
    assert exc_info.value.quantidade == -10

def test_remover_produto_invalido(estoque: Estoque):
    with pytest.raises(ProdutoNaoEncontradoError) as exc_info:
        estoque.remover("PR100", 10)
    assert exc_info.value.codigo == "PR100"

def test_remover_produto_estoque_insuficiente(estoque: Estoque):
    with pytest.raises(EstoqueInsuficienteError) as exc_info:
            estoque.remover("PR1", 1000)
    assert exc_info.value.codigo == "PR1"
    assert exc_info.value.disponivel == 30
    assert exc_info.value.solicitado == 1000 

@pytest.mark.parametrize("codigo, quantidade_esperada",
    [
        ("PR1", 30),
        ("PR2", 5),
    ]    
)
def test_quantidade(estoque: Estoque, codigo: str, quantidade_esperada: int):
    quantidade = estoque.quantidade(codigo)
    assert quantidade == quantidade_esperada

def test_quantidade_produto_nao_encontrado(estoque: Estoque):
    with pytest.raises(ProdutoNaoEncontradoError) as exc_info:
        estoque.quantidade("PR100")
    assert exc_info.value.codigo == "PR100"

@pytest.mark.parametrize("codigo, valor_esperado",
    [
        ("PR1", True),
        ("PR2", True),
        ("PR100", False)
    ]    
)
def test_contains(estoque: Estoque, codigo: str, valor_esperado):
    encotrado = codigo in estoque

    assert encotrado == valor_esperado

def test_processar_pedido(estoque: Estoque):

    lista_pedido = [
        ("PR1",5),
        ("PR2",1),
    ]

    processar_pedido(estoque, lista_pedido)

    assert estoque.quantidades == {"PR1": 25, "PR2":4}


@pytest.mark.parametrize("item_falho, tipo_causa", [
    (("PR2", 1000), EstoqueInsuficienteError),  
    (("PR2",-1000), QuantidadeInvalidaError),
    (("PR100", 10) , ProdutoNaoEncontradoError),        
])
def test_processar_pedido_pedido_recusado(estoque: Estoque, item_falho: Produto, tipo_causa: type[EstoqueError]):

    lista_pedido = [
        ("PR1",1),
        (item_falho),
    ]

    with pytest.raises(PedidoRecusadoError) as exc_info:
        processar_pedido(estoque, lista_pedido)

    assert estoque.quantidades == {"PR1": 30, "PR2":5}

    assert exc_info.value.codigo == item_falho[0]  
    assert exc_info.value.indice == 1 
    assert isinstance(exc_info.value.__cause__, tipo_causa)

        



    
    


    








    
