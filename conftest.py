from estoque import Estoque, Produto
import pytest


@pytest.fixture
def estoque_vazio():
    estoque = Estoque()
    return estoque

