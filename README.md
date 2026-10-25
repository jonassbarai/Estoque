# Controle de Estoque

Exercício integrador de Python, parte dos meus estudos da linguagem. Simula um controle de estoque simples com produtos, entradas, saídas e pedidos processados de forma atômica (tudo ou nada).

## Conceitos praticados

- Hierarquia de exceções customizadas, com atributos próprios e encadeamento (`raise ... from`)
- `dataclass` imutável (`frozen=True`) com validação no `__post_init__`
- `@property` e métodos especiais (`__contains__`)
- Context manager com `@contextmanager` para transações com rollback
- Testes com `pytest`: fixtures em `conftest.py`, `parametrize` e `unittest.mock`

## Estrutura

```
estoque/
├── estoque.py          # exceções, Produto, Estoque e processar_pedido
├── conftest.py         # fixtures compartilhadas dos testes
├── test_estoque.py     # testes
├── requirements.txt
└── README.md
```

## Funcionalidades

### Exceções

Todas herdam de `EstoqueError`:

| Exceção | Atributos | Quando ocorre |
|---|---|---|
| `ProdutoNaoEncontradoError` | `codigo` | Código não cadastrado no estoque |
| `EstoqueInsuficienteError` | `codigo`, `disponivel`, `solicitado` | Remoção maior que o saldo |
| `QuantidadeInvalidaError` | `quantidade` | Quantidade zero ou negativa |
| `PedidoRecusadoError` | `indice` | Falha em um item do pedido (posição do item) |

### `Produto`

Dataclass imutável com `codigo`, `nome` e `preco`. Rejeita preço zero ou negativo com `ValueError`.

### `Estoque`

| Membro | Descrição |
|---|---|
| `adicionar(produto, quantidade)` | Cadastra o produto ou soma à quantidade existente |
| `remover(codigo, quantidade)` | Valida quantidade, existência e saldo, nessa ordem |
| `quantidade(codigo)` | Retorna o saldo do produto |
| `valor_total` | Propriedade com a soma de `preco × quantidade` |
| `"P01" in estoque` | Verifica se o produto está cadastrado |
| `transacao()` | Context manager: se ocorrer erro dentro do `with`, restaura as quantidades e relança a exceção |

### `processar_pedido(estoque, itens)`

Recebe uma lista de pares `(codigo, quantidade)` e remove todos dentro de uma transação. Se algum item falhar, lança `PedidoRecusadoError` com a posição do item e a causa original, e o estoque permanece exatamente como estava.

## Exemplo de uso

```python
from estoque import Estoque, Produto

estoque = Estoque()
estoque.adicionar(Produto("P01", "Caneta", 2.5), 100)
estoque.adicionar(Produto("P02", "Caderno", 15.0), 20)

print(estoque.valor_total)       # 550.0
print("P01" in estoque)          # True

estoque.remover("P01", 10)
print(estoque.quantidade("P01")) # 90
```

## Como executar

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

## Status

- [x] Exceções customizadas
- [x] `Produto`
- [x] `Estoque`: `adicionar`, `remover`, `quantidade`, `valor_total`, `__contains__`
- [x] `transacao()` com rollback
- [x] `processar_pedido`
- [x] Testes com pytest
- [ ] Bônus: notificação de estoque baixo com `Mock`
