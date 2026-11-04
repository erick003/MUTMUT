# Tutorial MUTMUT

Este tutorial demonstra como usar testes de mutação para avaliar a capacidade de uma suíte de testes detectar alterações na lógica do programa.

## 1. Preparação do ambiente

```bash
mkdir mutmut-pratico
cd mutmut-pratico
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest mutmut
```

No Windows, ative o ambiente virtual com:

```powershell
.venv\Scripts\activate
```

## 2. Código da regra de negócio

A implementação está em [loja.py](loja.py):

```python
def calcular_desconto(valor_total: float, fidelidade: bool) -> float:
    """Aplica desconto de acordo com o valor da compra e a fidelidade."""
    if valor_total > 100.0:
        desconto = 0.10
    else:
        desconto = 0.0

    if fidelidade:
        desconto += 0.05

    return valor_total * (1.0 - desconto)
```

## 3. Primeira suíte de testes

Os testes da suíte final estão em [test_loja.py](test_loja.py) e cobrem o limite de R$ 100,00 e a combinação de compra acima de R$ 100,00 com fidelidade.

```bash
pytest
```

Resultado esperado:

```text
5 passed
```

## 4. Executando o mutmut

O projeto inclui [setup.cfg](setup.cfg), necessário nas versões atuais do mutmut:

```ini
[mutmut]
source_paths=loja.py
```

Execute a análise com:

```bash
mutmut run
```

Em versões antigas, o mesmo caminho pode ser informado diretamente:

```bash
mutmut run --paths-to-mutate=loja.py
```

O mutmut gera versões pequenas e deliberadamente incorretas da implementação:

- `Killed`: o teste detectou a alteração.
- `Survived`: os testes não detectaram a alteração.
- `Suspicious`: os testes não produziram um resultado confiável.
- `Timeout`: a execução ultrapassou o limite de tempo.

## 5. Inspecionando sobreviventes

```bash
mutmut results
mutmut show 1
mutmut show 3
```

Um mutante comum troca `>` por `>=`, revelando que o valor exatamente igual a R$ 100,00 não é coberto. Outro pode trocar `if fidelidade:` por `if not fidelidade:`, revelando que falta testar a combinação de compra acima de R$ 100,00 com fidelidade.

## 6. Casos que eliminam os mutantes

```python
# Exatamente 100.0 não recebe 10% de desconto.
def test_valor_exato_de_borda_100():
    assert calcular_desconto(100.0, fidelidade=False) == 100.0

# 200 - 15% (10% + 5%) = 170.
def test_compra_acima_de_100_com_fidelidade():
    assert calcular_desconto(200.0, fidelidade=True) == 170.0
```

Execute novamente:

```bash
mutmut run --paths-to-mutate=loja.py
```

Uma suíte com todos os mutantes eliminados possui cobertura de linha e capacidade real de detectar alterações na regra de negócio.

## Comandos úteis

```bash
# Reexecuta todos os mutantes, ignorando o cache.
mutmut run --rerun-all

# Aplica um mutante ao arquivo original.
mutmut apply <ID>

# Desfaz alterações locais feitas pelo exercício.
git checkout -- loja.py

# Gera um relatório HTML estático.
mutmut html
```

Observação: a disponibilidade e a sintaxe de alguns comandos podem variar conforme a versão do mutmut.