"""Testes do provedor de taxas (critério CA-06: API acessada corretamente)."""
import io
import json
import unittest
import urllib.error
from unittest import mock

from conversor import taxas
from conversor.core import MOEDAS_SUPORTADAS
from conversor.taxas import (
    FONTE_API,
    FONTE_FALLBACK,
    TAXAS_FALLBACK,
    buscar_taxas_api,
    obter_taxas,
)

URLOPEN = "conversor.taxas.urllib.request.urlopen"
RATES_API = {"USD": 1, "EUR": 0.9, "BRL": 5.5, "GBP": 0.8, "JPY": 150, "CAD": 1.4, "ARS": 1000}
CORPO_OK = {"result": "success", "rates": {**RATES_API, "CHF": 0.85}}  # CHF não é suportada


def corpo_com(**alteracoes):
    """Resposta de sucesso com as taxas de RATES_API alteradas (None remove a moeda)."""
    rates = {**RATES_API, **alteracoes}
    return {"result": "success", "rates": {m: t for m, t in rates.items() if t is not None}}


def resposta_falsa(corpo):
    """Simula a resposta de ``urlopen`` (BytesIO já funciona como gerenciador de contexto)."""
    return io.BytesIO(json.dumps(corpo).encode("utf-8"))


def buscador_com_erro(erro):
    def buscador():
        raise erro

    return buscador


class TestBuscarTaxasApi(unittest.TestCase):
    def test_consulta_a_url_com_timeout_e_filtra_moedas(self):
        with mock.patch(URLOPEN, return_value=resposta_falsa(CORPO_OK)) as urlopen:
            resultado = buscar_taxas_api()
        urlopen.assert_called_once_with(taxas.URL_API, timeout=taxas.TIMEOUT_SEGUNDOS)
        self.assertEqual(resultado, RATES_API)

    def test_resultado_sem_sucesso(self):
        corpo = {"result": "error", "rates": {}}
        with mock.patch(URLOPEN, return_value=resposta_falsa(corpo)):
            with self.assertRaises(ValueError):
                buscar_taxas_api()

    def test_moeda_ausente(self):
        for moeda in MOEDAS_SUPORTADAS:
            with self.subTest(moeda=moeda):
                with mock.patch(URLOPEN, return_value=resposta_falsa(corpo_com(**{moeda: None}))):
                    with self.assertRaises(ValueError):
                        buscar_taxas_api()

    def test_taxa_invalida(self):
        for valor in [0, -1, "5", True]:
            with self.subTest(valor=valor):
                with mock.patch(URLOPEN, return_value=resposta_falsa(corpo_com(BRL=valor))):
                    with self.assertRaises(ValueError):
                        buscar_taxas_api()


class TestObterTaxas(unittest.TestCase):
    def test_usa_api_quando_disponivel(self):
        resultado, fonte = obter_taxas(buscador=lambda: dict(RATES_API, BRL=3))
        self.assertEqual(fonte, FONTE_API)
        self.assertEqual(resultado["BRL"], 3)

    def test_fallback_em_erro_de_rede(self):
        resultado, fonte = obter_taxas(buscador=buscador_com_erro(urllib.error.URLError("sem internet")))
        self.assertEqual(fonte, FONTE_FALLBACK)
        self.assertEqual(resultado, TAXAS_FALLBACK)

    def test_fallback_em_timeout(self):
        _, fonte = obter_taxas(buscador=buscador_com_erro(TimeoutError()))
        self.assertEqual(fonte, FONTE_FALLBACK)

    def test_fallback_em_resposta_invalida(self):
        _, fonte = obter_taxas(buscador=buscador_com_erro(json.JSONDecodeError("x", "", 0)))
        self.assertEqual(fonte, FONTE_FALLBACK)

    def test_fallback_retorna_copia(self):
        resultado, _ = obter_taxas(buscador=buscador_com_erro(OSError()))
        resultado["BRL"] = 999
        self.assertNotEqual(TAXAS_FALLBACK["BRL"], 999)

    def test_fallback_cobre_moedas_suportadas(self):
        self.assertEqual(set(TAXAS_FALLBACK), set(MOEDAS_SUPORTADAS))


if __name__ == "__main__":
    unittest.main()
