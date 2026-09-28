"""Obtenção das taxas de câmbio (API pública com fallback pré-definido)."""
import json
import urllib.request

from .core import MOEDAS_SUPORTADAS

URL_API = "https://open.er-api.com/v6/latest/USD"
NOME_API = "ExchangeRate-API (open.er-api.com)"
TIMEOUT_SEGUNDOS = 5

# Unidades de cada moeda por 1 USD. Usadas quando a API está indisponível.
TAXAS_FALLBACK = {
    "USD": 1.0,
    "EUR": 0.92,
    "BRL": 5.00,
    "GBP": 0.76,
    "JPY": 155.0,
    "CAD": 1.41,
    "ARS": 1500.0,
}

FONTE_API = "api"
FONTE_FALLBACK = "fallback"


def buscar_taxas_api(url=URL_API, timeout=TIMEOUT_SEGUNDOS):
    """Consulta a API e devolve ``{moeda: taxa}`` só com as moedas suportadas.

    Raises:
        ValueError: resposta sem sucesso ou sem alguma moeda suportada
            (``json.JSONDecodeError`` também herda de ``ValueError``).
        OSError: falhas de rede (``URLError`` e timeout herdam de ``OSError``).
    """
    with urllib.request.urlopen(url, timeout=timeout) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))
    if dados.get("result") != "success":
        raise ValueError("A API não retornou sucesso.")
    rates = dados.get("rates", {})
    taxas = {}
    for moeda in MOEDAS_SUPORTADAS:
        taxa = rates.get(moeda)
        if not isinstance(taxa, (int, float)) or isinstance(taxa, bool) or taxa <= 0:
            raise ValueError(f"Taxa ausente ou inválida para {moeda}.")
        taxas[moeda] = taxa
    return taxas


def obter_taxas(buscador=buscar_taxas_api):
    """Devolve ``(taxas, fonte)``; cai para :data:`TAXAS_FALLBACK` se a API falhar.

    ``fonte`` é :data:`FONTE_API` ou :data:`FONTE_FALLBACK`. O parâmetro
    ``buscador`` existe para permitir injeção nos testes.
    """
    try:
        return buscador(), FONTE_API
    except (OSError, ValueError):
        return dict(TAXAS_FALLBACK), FONTE_FALLBACK
