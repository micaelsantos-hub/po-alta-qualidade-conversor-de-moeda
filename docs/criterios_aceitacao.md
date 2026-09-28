# Critérios de Aceitação — Conversor de Moedas

**História de usuário:** *Como usuário, quero converter um valor entre moedas para saber quanto ele vale na moeda de destino.*

**Moedas suportadas (7):** USD, EUR, BRL, GBP, JPY, CAD, ARS.

| ID | Critério | Como é verificado |
|----|----------|-------------------|
| CA-01 | O usuário pode selecionar a moeda de origem e a moeda de destino entre as 7 moedas suportadas. | `tests/test_web.py::TestFormulario`, `TestConversaoPeloFormulario.test_mantem_selecao_do_usuario`; `tests/test_core.py::TestMoedasSuportadas` |
| CA-02 | O usuário pode informar a quantidade na moeda de origem (aceita `10.50` e `10,50`). | `tests/test_web.py::TestFormulario`, `test_virgula_decimal`; `tests/test_core.py::test_aceita_virgula_decimal` |
| CA-03 | O sistema exibe o valor equivalente na moeda de destino. | `tests/test_core.py::TestConversaoPositiva`, `TestMoedasSuportadas`; `tests/test_web.py::test_exibe_resultado_com_duas_casas`, `test_converte_com_moeda_nova` |
| CA-04 | O resultado tem precisão de, no mínimo, duas casas decimais. | `tests/test_core.py::test_resultado_tem_duas_casas_decimais`, `test_sem_erro_de_ponto_flutuante`, `test_todos_os_pares_de_moedas_convertem` |
| CA-05 | O resultado é arredondado corretamente (metade para cima, `ROUND_HALF_UP`). | `tests/test_core.py::TestPrecisaoEArredondamento` |
| CA-06 | As taxas vêm de uma API pública; se ela falhar (rede, timeout, resposta inválida ou moeda ausente), o sistema usa taxas pré-definidas e informa a fonte ao usuário pelo nome. | `tests/test_taxas.py`; `tests/test_web.py::test_indica_fonte_*`, `TestIntegracaoComFallback` |
| CA-07 | Entradas inválidas (valor vazio, não numérico, negativo, acima de 1 trilhão; moeda desconhecida) são rejeitadas com mensagem clara. | `tests/test_core.py::TestValorInvalido`, `TestMoedaInvalida` |
| CA-08 | A interface responde de forma adequada a erros: mostra a mensagem, mantém o que o usuário digitou, nunca retorna erro 500 e escapa o conteúdo digitado. | `tests/test_web.py::TestErrosNaInterface` |

## Cenários (Dado / Quando / Então)

### CA-01 — Seleção de moedas
```gherkin
Cenário: Escolher moedas de origem e destino
  Dado que abri a página do conversor
  Quando vejo os campos "Moeda de origem" e "Moeda de destino"
  Então cada campo lista as 7 moedas (USD, EUR, BRL, GBP, JPY, CAD e ARS) com código e nome
  E o padrão é USD como origem e BRL como destino

Cenário: A seleção é mantida após converter
  Dado que escolhi EUR como origem e USD como destino
  Quando clico em "Converter"
  Então a página exibe o resultado com EUR e USD ainda selecionados
```

### CA-02 — Entrada do valor
```gherkin
Cenário: Informar valor com ponto ou vírgula
  Dado que estou no formulário
  Quando informo "10,50" ou "10.50" em "Valor"
  Então o sistema interpreta o valor como 10,50 nos dois casos
```

### CA-03 — Exibição do equivalente
```gherkin
Cenário: Converter entre duas moedas
  Dado que as taxas são 1 USD = 5,00 BRL
  Quando converto 100 USD para BRL
  Então o resultado exibido é "100.00 USD = 500.00 BRL"

Cenário: Converter entre duas moedas que não são o dólar
  Dado que 1 USD = 0,80 GBP e 1 USD = 5,00 BRL
  Quando converto 80 GBP para BRL
  Então o sistema converte via USD e exibe 500.00 BRL

Cenário: Mesma moeda
  Dado que origem e destino são EUR
  Quando converto 10,50 EUR
  Então o resultado é 10.50 EUR
```

### CA-04 — Precisão
```gherkin
Cenário: Duas casas decimais
  Dado qualquer par de moedas suportadas
  Quando converto 1 unidade
  Então o resultado tem exatamente duas casas decimais

Cenário: Sem erro de ponto flutuante
  Dado que 1 USD = 3 EUR
  Quando converto 1,1 USD para EUR
  Então o resultado é 3.30 (e não 3.3000000000000003)
```

### CA-05 — Arredondamento
```gherkin
Cenário: Metade arredonda para cima
  Dado origem e destino iguais a USD
  Quando converto 0,005
  Então o resultado é 0.01

Cenário: Abaixo da metade arredonda para baixo
  Dado origem e destino iguais a USD
  Quando converto 0,004
  Então o resultado é 0.00
```

### CA-06 — Taxas da API com fallback
```gherkin
Cenário: API disponível
  Dado que a API ExchangeRate-API responde com sucesso e com as 7 moedas
  Quando converto qualquer valor
  Então uso as taxas da API
  E a tela mostra "Taxas atualizadas via ExchangeRate-API (open.er-api.com)"

Cenário: API indisponível
  Dado que a API falha por erro de rede, timeout, resposta inválida ou moeda ausente
  Quando converto qualquer valor
  Então uso as taxas pré-definidas
  E a tela mostra "Taxas pré-definidas: não foi possível consultar ExchangeRate-API (open.er-api.com)"
```

### CA-07 — Entradas inválidas
```gherkin
Esquema do Cenário: Valor inválido é rejeitado
  Dado que estou no formulário
  Quando informo o valor "<entrada>"
  Então vejo a mensagem de erro "<mensagem>"
  E nenhum resultado é exibido

  Exemplos:
    | entrada          | mensagem                                          |
    | abc              | Valor inválido: 'abc'.                            |
    | -5               | O valor não pode ser negativo.                    |
    | 1e5              | Valor inválido: '1e5'.                            |
    | 1000000000000,01 | O valor não pode ser maior que 1,000,000,000,000. |

Cenário: Moeda desconhecida
  Dado que a requisição traz a moeda "XXX" adulterada
  Quando o sistema tenta converter
  Então vejo "Moeda não suportada: XXX."
```

### CA-08 — Resposta da interface a erros
```gherkin
Cenário: Erro não derruba a página
  Dado que informei uma entrada inválida (ex.: "1e999" ou campos ausentes)
  Quando envio o formulário
  Então a resposta é 200 com a mensagem em um alerta (role="alert")
  E o que digitei continua no campo

Cenário: Conteúdo digitado é escapado
  Dado que informei "<script>alert(1)</script>" em "Valor"
  Quando envio o formulário
  Então o texto aparece escapado e nenhum script é executado
```

## Definição de Pronto (DoD)

- [x] Todos os critérios de aceitação implementados e cobertos por testes.
- [x] `python -m unittest discover` executa sem falhas.
- [x] Documentação técnica atualizada (`docs/documentacao_tecnica.md`).
- [x] Código e documentação revisados (`docs/revisao.md`).
- [x] Quadro Trello atualizado, com todos os cartões em **Done**.
