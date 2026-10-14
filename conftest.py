from estoque import Estoque, Produto
import pytest


@pytest.fixture
def estoque_vazio():
    estoque = Estoque()
    return estoque

@pytest.fixture
def estoque():
    estoque = Estoque()

    estoque.adicionar(Produto("PR1","PRODUTO1",10),30)
    estoque.adicionar(Produto("PR2","PRODUTO2",6),5)

    return estoque


