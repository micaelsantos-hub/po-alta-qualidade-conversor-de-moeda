"""Testes unitários do núcleo de conversão (critérios CA-03 a CA-05 e CA-07)."""
import unittest
from decimal import Decimal

from conversor.core import (
    MOEDAS,
    MOEDAS_SUPORTADAS,
    MoedaInvalidaError,
    ValorInvalidoError,
    converter,
    interpretar_valor,
)

TAXAS = {"USD": 1.0, "EUR": 0.92, "BRL": 5.0, "GBP": 0.8, "JPY": 150.0, "CAD": 1.25, "ARS": 1000.0}


class TestConversaoPositiva(unittest.TestCase):
    def test_usd_para_brl(self):
        self.assertEqual(converter("100", "USD", "BRL", TAXAS), Decimal("500.00"))

    def test_brl_para_usd(self):
        self.assertEqual(converter("500", "BRL", "USD", TAXAS), Decimal("100.00"))

    def test_eur_para_brl_passa_por_usd(self):
        # 92 EUR = 100 USD = 500 BRL
        self.assertEqual(converter("92", "EUR", "BRL", TAXAS), Decimal("500.00"))

    def test_mesma_moeda_mantem_valor(self):
        self.assertEqual(converter("10.50", "EUR", "EUR", TAXAS), Decimal("10.50"))

    def test_zero_resulta_zero(self):
        self.assertEqual(converter("0", "USD", "BRL", TAXAS), Decimal("0.00"))

    def test_aceita_virgula_decimal(self):
        self.assertEqual(converter("10,50", "USD", "BRL", TAXAS), Decimal("52.50"))

    def test_aceita_moeda_em_minusculas_e_com_espacos(self):
        self.assertEqual(converter("1", " usd ", "brl", TAXAS), Decimal("5.00"))

    def test_aceita_float_e_int(self):
        self.assertEqual(converter(2, "USD", "BRL", TAXAS), Decimal("10.00"))
        self.assertEqual(converter(2.5, "USD", "BRL", TAXAS), Decimal("12.50"))


class TestMoedasSuportadas(unittest.TestCase):
    def test_sete_moedas_suportadas(self):
        self.assertEqual(
            set(MOEDAS_SUPORTADAS), {"USD", "EUR", "BRL", "GBP", "JPY", "CAD", "ARS"}
        )

    def test_toda_moeda_tem_nome(self):
        for codigo, nome in MOEDAS.items():
            with self.subTest(codigo=codigo):
                self.assertTrue(nome.strip())

    def test_conversoes_das_novas_moedas(self):
        casos = [
            ("100", "USD", "GBP", "80.00"),
            ("100", "USD", "JPY", "15000.00"),
            ("100", "USD", "CAD", "125.00"),
            ("1", "USD", "ARS", "1000.00"),
            ("150", "JPY", "USD", "1.00"),
            ("80", "GBP", "BRL", "500.00"),  # via USD: 80 GBP = 100 USD = 500 BRL
            ("1000", "ARS", "CAD", "1.25"),
        ]
        for valor, origem, destino, esperado in casos:
            with self.subTest(origem=origem, destino=destino):
                self.assertEqual(converter(valor, origem, destino, TAXAS), Decimal(esperado))

    def test_todos_os_pares_de_moedas_convertem(self):
        for origem in MOEDAS_SUPORTADAS:
            for destino in MOEDAS_SUPORTADAS:
                with self.subTest(origem=origem, destino=destino):
                    resultado = converter("1", origem, destino, TAXAS)
                    self.assertEqual(resultado.as_tuple().exponent, -2)
                    self.assertGreaterEqual(resultado, 0)

    def test_ida_e_volta_preserva_valor_em_moeda_de_taxa_exata(self):
        ida = converter("100", "USD", "GBP", TAXAS)
        self.assertEqual(converter(ida, "GBP", "USD", TAXAS), Decimal("100.00"))


class TestPrecisaoEArredondamento(unittest.TestCase):
    def test_resultado_tem_duas_casas_decimais(self):
        resultado = converter("1", "USD", "EUR", TAXAS)
        self.assertEqual(resultado.as_tuple().exponent, -2)

    def test_arredonda_para_cima_na_metade(self):
        # 0.005 exato -> 0.01 (a metade arredonda para cima)
        self.assertEqual(converter("0.005", "USD", "USD", TAXAS), Decimal("0.01"))

    def test_arredonda_para_baixo_abaixo_da_metade(self):
        self.assertEqual(converter("0.004", "USD", "USD", TAXAS), Decimal("0.00"))

    def test_divisao_nao_exata_e_arredondada(self):
        # 1 BRL = 0.2 USD = 0.184 EUR -> 0.18
        self.assertEqual(converter("1", "BRL", "EUR", TAXAS), Decimal("0.18"))

    def test_sem_erro_de_ponto_flutuante(self):
        # com float, 1.1 * 3 = 3.3000000000000003
        taxas = {"USD": 1.0, "EUR": 3.0, "BRL": 5.0}
        self.assertEqual(converter("1.1", "USD", "EUR", taxas), Decimal("3.30"))

    def test_valor_grande(self):
        self.assertEqual(
            converter("1000000000", "USD", "BRL", TAXAS), Decimal("5000000000.00")
        )


class TestValorInvalido(unittest.TestCase):
    def test_valores_rejeitados(self):
        entradas = ["abc", "", "   ", "-1", "-0,01", "NaN", "Infinity", "1e", "1,2,3", "1e5", "1_000", "0x10", None, True]
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValorInvalidoError):
                    interpretar_valor(entrada)

    def test_valor_acima_do_maximo_e_rejeitado(self):
        for entrada in ["1000000000000.01", "1" + "0" * 30]:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValorInvalidoError):
                    converter(entrada, "USD", "BRL", TAXAS)

    def test_valor_no_maximo_e_aceito(self):
        self.assertEqual(
            converter("1000000000000", "USD", "USD", TAXAS), Decimal("1000000000000.00")
        )

    def test_converter_propaga_valor_invalido(self):
        with self.assertRaises(ValorInvalidoError):
            converter("abc", "USD", "BRL", TAXAS)


class TestMoedaInvalida(unittest.TestCase):
    def test_origem_desconhecida(self):
        with self.assertRaises(MoedaInvalidaError):
            converter("1", "XXX", "BRL", TAXAS)

    def test_destino_desconhecido(self):
        with self.assertRaises(MoedaInvalidaError):
            converter("1", "USD", "CHF", TAXAS)

    def test_moeda_vazia_ou_nao_texto(self):
        for moeda in ["", "  ", None, 123]:
            with self.subTest(moeda=moeda):
                with self.assertRaises(MoedaInvalidaError):
                    converter("1", moeda, "BRL", TAXAS)

    def test_moeda_suportada_sem_taxa(self):
        with self.assertRaises(MoedaInvalidaError):
            converter("1", "USD", "EUR", {"USD": 1.0})
        with self.assertRaises(MoedaInvalidaError):
            converter("1", "USD", "GBP", {k: v for k, v in TAXAS.items() if k != "GBP"})

    def test_taxa_nao_positiva(self):
        with self.assertRaises(MoedaInvalidaError):
            converter("1", "USD", "EUR", {"USD": 1.0, "EUR": 0})


if __name__ == "__main__":
    unittest.main()
