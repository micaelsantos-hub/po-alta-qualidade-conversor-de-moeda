# Agile Docs & Code — Conversor de Moedas

Atividade de simulação de uma sprint Scrum: conversor de moedas (USD, EUR, BRL, GBP, JPY, CAD e ARS)
com interface web em Flask, testes unitários com `unittest` e documentação técnica.

- **Quadro Trello:** https://trello.com/b/KkuWlxO0/agile-docs-code-sprint
- **Repositório:** https://github.com/micaelsantos-hub/po-alta-qualidade-conversor-de-moeda

## Executar

Requer Python 3.10+.

```bash
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000. As taxas vêm de uma API pública; sem internet, a
aplicação usa taxas pré-definidas e avisa na tela.

## Testes

```bash
python -m unittest discover -v
```

54 testes, todos offline (a API é simulada).

## Estrutura

```
app.py                       ponto de entrada
conversor/core.py            regra de negócio (Decimal, validação, arredondamento)
conversor/taxas.py           API de taxas com fallback
conversor/web.py             aplicação Flask
conversor/templates/         página HTML
tests/                       testes unitários
docs/criterios_aceitacao.md  critérios de aceitação e Definição de Pronto
docs/documentacao_tecnica.md descrição, fluxo, interfaces, armazenamento, APIs
docs/revisao.md              feedback da revisão e sugestões de melhoria
docs/guia_trello.md          montagem do quadro Trello
docs/reflexao_scrum.md       reflexão sobre o processo
```

## Créditos

Taxas de câmbio: [ExchangeRate-API](https://www.exchangerate-api.com) (endpoint aberto).
