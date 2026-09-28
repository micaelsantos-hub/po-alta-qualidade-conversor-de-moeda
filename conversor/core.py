"""Núcleo de conversão de moedas.

Todas as contas usam ``decimal.Decimal`` para evitar os erros de
representação do ``float`` (ex.: ``0.1 + 0.2 != 0.3``).
"""
import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

MOEDAS = {
    "USD": "Dólar americano",
    "EUR": "Euro",
    "BRL": "Real brasileiro",
    "GBP": "Libra esterlina",
    "JPY": "Iene japonês",
    "CAD": "Dólar canadense",
    "ARS": "Peso argentino",
}
MOEDAS_SUPORTADAS = tuple(MOEDAS)
CASAS_DECIMAIS = Decimal("0.01")
VALOR_MAXIMO = Decimal("1000000000000")  # 1 trilhão; evita estouro da precisão do Decimal
_PADRAO_NUMERO = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)")


class ConversorError(Exception):
    """Erro base do conversor."""


class ValorInvalidoError(ConversorError):
    """O valor informado não é um número válido e não negativo."""


class MoedaInvalidaError(ConversorError):
    """A moeda informada não é suportada ou não tem taxa disponível."""


def interpretar_valor(texto):
    """Converte a entrada do usuário em ``Decimal``.

    Aceita ``int``, ``float``, ``Decimal`` ou ``str``; em strings, tanto
    ``10.50`` quanto ``10,50`` são aceitos (notação científica, separador de
    milhar e prefixos como ``0x`` são rejeitados).

    Raises:
        ValorInvalidoError: se o valor não for numérico, for infinito/NaN,
            negativo ou maior que :data:`VALOR_MAXIMO`.
    """
    if isinstance(texto, bool) or texto is None:
        raise ValorInvalidoError("Informe um valor numérico.")
    if isinstance(texto, str):
        texto = texto.strip().replace(",", ".")
        if not texto:
            raise ValorInvalidoError("Informe um valor numérico.")
        if not _PADRAO_NUMERO.fullmatch(texto):
            raise ValorInvalidoError(f"Valor inválido: {texto!r}.")
    try:
        valor = Decimal(str(texto))
    except InvalidOperation:
        raise ValorInvalidoError(f"Valor inválido: {texto!r}.") from None
    if not valor.is_finite():
        raise ValorInvalidoError("O valor deve ser um número finito.")
    if valor < 0:
        raise ValorInvalidoError("O valor não pode ser negativo.")
    if valor > VALOR_MAXIMO:
        raise ValorInvalidoError(f"O valor não pode ser maior que {VALOR_MAXIMO:,}.")
    return valor


def normalizar_moeda(codigo, taxas):
    """Devolve o código da moeda em maiúsculas, validando-o contra ``taxas``."""
    if not isinstance(codigo, str):
        raise MoedaInvalidaError("Moeda inválida.")
    codigo = codigo.strip().upper()
    if codigo not in MOEDAS_SUPORTADAS or codigo not in taxas:
        raise MoedaInvalidaError(f"Moeda não suportada: {codigo or '(vazia)'}.")
    return codigo


def converter(valor, origem, destino, taxas):
    """Converte ``valor`` de ``origem`` para ``destino``.

    Args:
        valor: quantidade na moeda de origem (ver :func:`interpretar_valor`).
        origem: código da moeda de origem (ex.: ``"USD"``).
        destino: código da moeda de destino (ex.: ``"BRL"``).
        taxas: mapa ``{moeda: unidades dessa moeda por 1 USD}``.

    Returns:
        ``Decimal`` arredondado para 2 casas decimais (``ROUND_HALF_UP``).

    Raises:
        ValorInvalidoError: valor inválido.
        MoedaInvalidaError: moeda não suportada ou sem taxa.
    """
    valor = interpretar_valor(valor)
    origem = normalizar_moeda(origem, taxas)
    destino = normalizar_moeda(destino, taxas)
    taxa_origem = Decimal(str(taxas[origem]))
    taxa_destino = Decimal(str(taxas[destino]))
    if taxa_origem <= 0 or taxa_destino <= 0:
        raise MoedaInvalidaError("Taxa de conversão inválida.")
    resultado = valor / taxa_origem * taxa_destino
    return resultado.quantize(CASAS_DECIMAIS, rounding=ROUND_HALF_UP)
