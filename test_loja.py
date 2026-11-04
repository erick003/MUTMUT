import pytest

from loja import calcular_desconto


def test_compra_acima_de_100_sem_fidelidade():
    assert calcular_desconto(200.0, fidelidade=False) == 180.0


def test_compra_abaixo_de_100_com_fidelidade():
    assert calcular_desconto(50.0, fidelidade=True) == 47.5


def test_valor_exato_de_borda_100():
    assert calcular_desconto(100.0, fidelidade=False) == 100.0


def test_valor_acima_do_limite_recebe_desconto():
    assert calcular_desconto(100.01, fidelidade=False) == pytest.approx(90.009)


def test_compra_acima_de_100_com_fidelidade():
    assert calcular_desconto(200.0, fidelidade=True) == 170.0
