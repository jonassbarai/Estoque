import pytest
from estoque import Estoque, Produto, QuantidadeInvalidaError


def test_adicionar_produto(estoque_vazio: Estoque):
    produto = Produto("PR1-TESTE","PRODUTO TESTE", 15.69)
    estoque_vazio.adicionar(produto, 10)
    estoque_vazio.adicionar(produto, 10)

    assert estoque_vazio.quantidades == {"PR1-TESTE": 20}
    assert estoque_vazio.produtos == {'PR1-TESTE': Produto(codigo='PR1-TESTE', nome='PRODUTO TESTE', preco=15.69)}


def test_adicionar_produto_quantidade_invalida(estoque_vazio): 
    with pytest.raises(QuantidadeInvalidaError) as exc_info:
        estoque_vazio.adicionar(Produto("PR1-TESTE","PRODUTO TESTE", 15.69), -10)

    assert exc_info.value.quantidade == -10

def test_remover_produto(estoque: Estoque):
    estoque.remover("PR1", 10)
    assert  estoque.quantidades == {"PR1": 20, "PR2": 5}





    
