def calcular_desconto(valor_total: float, fidelidade: bool) -> float:
    """Aplica 10% de desconto acima de R$ 100,00 e 5% para clientes fiéis."""
    if valor_total > 100.0:
        desconto = 0.10
    else:
        desconto = 0.0

    if fidelidade:
        desconto += 0.05

    return valor_total * (1.0 - desconto)
