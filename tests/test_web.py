"""Testes da interface web (critérios CA-01, CA-02, CA-03 e CA-08)."""
import unittest
from unittest import mock

from conversor.core import MOEDAS
from conversor.web import create_app

TAXAS = {"USD": 1.0, "EUR": 0.92, "BRL": 5.0, "GBP": 0.8, "JPY": 150.0, "CAD": 1.25, "ARS": 1000.0}


def cliente(fonte="api"):
    app = create_app(provedor_taxas=lambda: (dict(TAXAS), fonte))
    app.testing = True
    return app.test_client()


def enviar(valor, origem="USD", destino="BRL", fonte="api"):
    resposta = cliente(fonte).post("/", data={"valor": valor, "origem": origem, "destino": destino})
    return resposta.get_data(as_text=True)


class TestFormulario(unittest.TestCase):
    def test_get_exibe_formulario_com_as_moedas(self):
        resposta = cliente().get("/")
        html = resposta.get_data(as_text=True)
        self.assertEqual(resposta.status_code, 200)
        for campo in ['name="valor"', 'name="origem"', 'name="destino"']:
            self.assertIn(campo, html)
        for moeda in MOEDAS:
            self.assertEqual(html.count(f'<option value="{moeda}"'), 2)  # origem e destino
        self.assertEqual(len(MOEDAS), 7)

    def test_opcoes_mostram_codigo_e_nome_da_moeda(self):
        html = cliente().get("/").get_data(as_text=True)
        self.assertIn("GBP — Libra esterlina", html)
        self.assertIn("JPY — Iene japonês", html)

    def test_get_nao_mostra_resultado_nem_erro(self):
        html = cliente().get("/").get_data(as_text=True)
        self.assertNotIn('id="resultado"', html)
        self.assertNotIn('id="erro"', html)


class TestConversaoPeloFormulario(unittest.TestCase):
    def test_exibe_resultado_com_duas_casas(self):
        html = enviar("100")
        self.assertIn('id="resultado"', html)
        self.assertIn("500.00 BRL", html)

    def test_virgula_decimal(self):
        self.assertIn("52.50 BRL", enviar("10,50"))

    def test_converte_com_moeda_nova(self):
        self.assertIn("80.00 GBP", enviar("100", origem="USD", destino="GBP"))
        self.assertIn("15000.00 JPY", enviar("100", origem="USD", destino="JPY"))

    def test_mantem_selecao_do_usuario(self):
        html = enviar("1", origem="EUR", destino="USD")
        self.assertIn('<option value="EUR" selected>', html)
        self.assertIn('<option value="USD" selected>', html)

    def test_indica_fonte_api(self):
        self.assertIn("Taxas atualizadas via ExchangeRate-API (open.er-api.com)", enviar("1"))

    def test_indica_fonte_fallback(self):
        html = enviar("1", fonte="fallback")
        self.assertIn("Taxas pré-definidas", html)
        self.assertIn("ExchangeRate-API (open.er-api.com)", html)


class TestErrosNaInterface(unittest.TestCase):
    def test_valor_invalido_mostra_erro(self):
        html = enviar("abc")
        self.assertIn('id="erro"', html)
        self.assertIn("Valor inválido", html)
        self.assertNotIn('id="resultado"', html)

    def test_valor_negativo_mostra_erro(self):
        self.assertIn("não pode ser negativo", enviar("-5"))

    def test_valor_gigante_nao_gera_erro_500(self):
        resposta = cliente().post("/", data={"valor": "1e999", "origem": "USD", "destino": "BRL"})
        self.assertEqual(resposta.status_code, 200)
        self.assertIn('id="erro"', resposta.get_data(as_text=True))

    def test_moeda_adulterada_mostra_erro(self):
        self.assertIn("Moeda não suportada", enviar("1", origem="XXX"))

    def test_campos_ausentes_nao_quebram(self):
        resposta = cliente().post("/", data={})
        self.assertEqual(resposta.status_code, 200)
        self.assertIn('id="erro"', resposta.get_data(as_text=True))

    def test_entrada_e_escapada_contra_xss(self):
        self.assertNotIn("<script>alert(1)</script>", enviar("<script>alert(1)</script>"))


class TestIntegracaoComFallback(unittest.TestCase):
    def test_sem_provedor_injetado_e_sem_rede_usa_fallback(self):
        with mock.patch("conversor.taxas.urllib.request.urlopen", side_effect=OSError("offline")):
            app = create_app()
            app.testing = True
            resposta = app.test_client().post("/", data={"valor": "100", "origem": "USD", "destino": "BRL"})
        html = resposta.get_data(as_text=True)
        self.assertIn("500.00 BRL", html)
        self.assertIn("pré-definidas", html)


if __name__ == "__main__":
    unittest.main()
