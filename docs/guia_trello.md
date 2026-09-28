# Guia do Quadro Trello — "Agile Docs & Code Sprint"

O Trello exige a sua conta, então o quadro precisa ser montado por você. Este
guia traz tudo pronto para copiar (5–10 minutos). No fim, tire um print do
quadro com todos os cartões em **Done** para a entrega.

## 1. Criar o quadro e as listas

1. Trello → **Criar** → **Criar quadro** → nome: `Agile Docs & Code Sprint`.
2. Crie as listas, nesta ordem: `Backlog`, `To Do`, `In Progress`, `Done`.
3. (Opcional) Crie as etiquetas: `Documentação` (azul), `Código` (verde), `Testes` (amarelo), `Revisão` (roxo).

## 2. Mapeamento com o Scrum

| Elemento Scrum | No quadro |
|----------------|-----------|
| Product Backlog | Lista **Backlog** (ordenada por prioridade, do topo para baixo) |
| Sprint Backlog | Lista **To Do** (itens escolhidos no Sprint Planning) |
| Trabalho em andamento | Lista **In Progress** (limite sugerido: 1–2 cartões por vez) |
| Incremento / Definição de Pronto | Lista **Done** (só entra o que cumpre a DoD de `criterios_aceitacao.md`) |
| Sprint Goal | Descrição do quadro: *"Entregar o conversor de moedas web, documentado, testado e revisado."* |
| Sprint Review / Retrospectiva | Cartão extra opcional `Retrospectiva` ou o texto de `docs/reflexao_scrum.md` |

## 3. Cartões do Backlog (em ordem de prioridade)

Crie os 5 cartões na lista **Backlog** com estas descrições e checklists.

### 1. Definir critérios de aceitação — `Documentação`
Descrição: Definir CA-01 a CA-08 do conversor e a Definição de Pronto.
Checklist: ☐ Critérios escritos ☐ Rastreabilidade com testes ☐ Definição de Pronto
Anexo/link: `docs/criterios_aceitacao.md`

### 2. Escrever a documentação técnica — `Documentação`
Descrição: Descrição, diagrama de fluxo, interfaces, armazenamento e APIs externas.
Checklist: ☐ Descrição ☐ Diagrama de fluxo ☐ Interfaces ☐ Armazenamento ☐ API externa
Anexo/link: `docs/documentacao_tecnica.md`

### 3. Desenvolver o código do conversor de moedas — `Código`
Descrição: Núcleo com Decimal, provedor de taxas com fallback e interface web Flask.
Checklist: ☐ core.py ☐ taxas.py ☐ web.py + template ☐ Executa em `python app.py`

### 4. Desenvolver os testes unitários — `Testes`
Descrição: Testes positivos e negativos cobrindo todos os critérios de aceitação.
Checklist: ☐ test_core ☐ test_taxas ☐ test_web ☐ 54 testes passando
Comando: `python -m unittest discover -v`

### 5. Revisão de código e documentação — `Revisão`
Descrição: Revisar, registrar achados e sugerir melhorias.
Checklist: ☐ Revisão do código ☐ Revisão da documentação ☐ Sugestões de melhoria
Anexo/link: `docs/revisao.md`

## 4. Movimentação sugerida (simulando a sprint)

Mova os cartões conforme o trabalho avança e registre cada passo em um comentário:

| Momento | Ação |
|---------|------|
| Sprint Planning | Mover os 5 cartões de **Backlog** para **To Do**. |
| Dia 1 | Cartão 1 → **In Progress** → **Done** (critérios definidos). |
| Dia 1–2 | Cartão 2 (documentação) → **In Progress** → **Done**. |
| Dia 2–3 | Cartão 3 (código) → **In Progress**; cartão 4 (testes) → **In Progress** em paralelo; ambos → **Done** com os testes verdes. |
| Dia 3 | Cartão 5 (revisão) → **In Progress** → **Done**. |
| Sprint Review | Print do quadro; anexar o link do repositório no cartão 3. |

Dica: use datas de entrega (**Datas**) nos cartões e marque cada item de
checklist ao concluir; o Trello mostra a barra de progresso no cartão.

## 5. Checklist de entrega

- [ ] Quadro com as 4 listas e os 5 cartões, todos em **Done**
- [ ] Print do quadro final
- [ ] Repositório no GitHub (ver `README.md`)
- [ ] Link do quadro Trello (Compartilhar → link) incluído no README
