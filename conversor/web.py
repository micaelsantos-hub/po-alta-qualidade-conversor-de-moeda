"""Interface web (Flask) do conversor de moedas."""
from flask import Flask, render_template, request

from . import taxas as modulo_taxas
from .core import MOEDAS, ConversorError, converter, interpretar_valor


def create_app(provedor_taxas=None):
    """Cria a aplicação Flask.

    Args:
        provedor_taxas: função sem argumentos que devolve ``(taxas, fonte)``.
            Por padrão usa :func:`conversor.taxas.obter_taxas`.
    """
    app = Flask(__name__)
    obter = provedor_taxas or modulo_taxas.obter_taxas

    @app.route("/", methods=["GET", "POST"])
    def index():
        contexto = {
            "moedas": MOEDAS,
            "valor": "",
            "origem": "USD",
            "destino": "BRL",
            "resultado": None,
            "valor_formatado": None,
            "erro": None,
            "fonte": None,
            "nome_api": modulo_taxas.NOME_API,
        }
        if request.method == "POST":
            contexto["valor"] = request.form.get("valor", "")
            contexto["origem"] = request.form.get("origem", "")
            contexto["destino"] = request.form.get("destino", "")
            taxas, contexto["fonte"] = obter()
            try:
                resultado = converter(
                    contexto["valor"], contexto["origem"], contexto["destino"], taxas
                )
                contexto["valor_formatado"] = f"{interpretar_valor(contexto['valor']):.2f}"
                contexto["resultado"] = f"{resultado:.2f}"
            except ConversorError as erro:
                contexto["erro"] = str(erro)
        return render_template("index.html", **contexto)

    return app
