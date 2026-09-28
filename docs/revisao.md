# Revisão de Código e Documentação

Revisão feita ao final da sprint, antes de mover o cartão para **Done**.

## O que a revisão encontrou e foi corrigido

| # | Problema | Como apareceu | Correção |
|---|----------|---------------|----------|
| 1 | **Erro 500 com valores enormes.** `1e30` ou `1e999` passavam pela validação e `Decimal.quantize` lançava `InvalidOperation` (estouro da precisão de 28 dígitos). | Teste manual com entradas extremas. | Limite `VALOR_MAXIMO` de 1 trilhão em `interpretar_valor`; testes `test_valor_acima_do_maximo_e_rejeitado` e `test_valor_gigante_nao_gera_erro_500`. |
| 2 | **Entradas aceitas por acidente pelo `Decimal`**: `1_000` (sublinhado) era lido como 1000. | Teste manual. | Regex estrita (`[+-]?(\d+\.?\d*\|\.\d+)`) antes de converter; `1e5`, `1_000` e `0x10` agora são rejeitados. |
| 3 | O roteiro pedia documentação da "funcionalidade login", mas todo o resto trata do conversor. | Leitura do roteiro. | Tratado como erro de digitação; documentou-se o conversor. |

## Revisão do código — pontos positivos

- Regra de negócio isolada (`core.py`), sem dependência de Flask ou rede.
- `Decimal` e `ROUND_HALF_UP` garantem precisão e arredondamento previsíveis.
- Provedor de taxas injetável (`create_app(provedor_taxas=...)`, `obter_taxas(buscador=...)`), o que permitiu testar tudo offline.
- Falha da API nunca derruba a aplicação e o usuário é informado da fonte.
- Jinja2 escapa a entrada do usuário (coberto por teste contra XSS).

## Sugestões de melhoria (backlog para a próxima sprint)

1. **Cache das taxas** (ex.: 1 hora): hoje cada conversão chama a API, o que adiciona latência (até 5 s no pior caso) e pode estourar o limite do plano gratuito.
2. **Mais moedas** *(parcialmente feito: já são 7)*: para ampliar, basta incluir a moeda em `MOEDAS` e `TAXAS_FALLBACK`; idealmente ler a lista da própria API. Observação: o JPY é exibido com 2 casas, embora o iene não tenha centavos na prática.
3. **Alertar a data das taxas de fallback**: elas são fixas e envelhecem; exibir "taxas de referência de <data>".
4. **Endpoint JSON** (`/api/converter`) para uso por outros sistemas.
5. **Servidor de produção** (gunicorn/waitress): `app.run` é apenas para desenvolvimento.
6. **Registro de logs** quando ocorrer fallback, para saber com que frequência a API falha.
7. **Medir cobertura** (`coverage run -m unittest`) e configurar CI (GitHub Actions) para rodar os testes a cada push.
8. **Teste de contrato opcional** contra a API real (marcado para não rodar por padrão), já que os testes atuais só validam o formato simulado.
9. **Acessibilidade e i18n**: rótulos já estão associados aos campos; falta testar leitores de tela e permitir exibir o resultado no formato local (`1.234,56`).
10. **Type hints** nas funções públicas.

## Revisão da documentação

- Fluxo, interfaces, armazenamento (nenhum) e API externa documentados em `documentacao_tecnica.md`.
- Critérios de aceitação rastreados até os testes em `criterios_aceitacao.md`.
- Limitação registrada: as taxas de fallback são aproximadas e o endpoint gratuito exige atribuição à fonte (ExchangeRate-API).
- Pendência: o README deve ser atualizado quando o repositório for publicado (URL do GitHub).
