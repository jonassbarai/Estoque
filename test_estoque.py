import pytest
from estoque import Estoque, Produto, QuantidadeInvalidaError


def test_adicionar_produto(estoque_vazio):
    estoque_vazio.adicionar(Produto("PR1-TESTE","PRODUTO TESTE", 15.69), 10)

    assert estoque_vazio.quantidades == {"PR1-TESTE": 10}
    assert estoque_vazio.produtos =={'PR1-TESTE': Produto(codigo='PR1-TESTE', nome='PRODUTO TESTE', preco=15.69)}

def test_adicionar_produto_quantidade_invalida(estoque_vazio): 
    with pytest.raises(QuantidadeInvalidaError) as exc_info:
        estoque_vazio.adicionar(Produto("PR1-TESTE","PRODUTO TESTE", 15.69), -10)

    assert exc_info.value.quantidade == -10


    
