# Reflexão sobre o Processo (Framework Scrum)

> Rascunho baseado no que aconteceu nesta sprint. Ajuste com as suas próprias
> impressões antes de entregar.

## Sprint Goal
Entregar o conversor de moedas web, documentado, testado e revisado.

## O que funcionou bem
- **Critérios de aceitação primeiro.** Com CA-01 a CA-08 definidos, os testes saíram quase diretos e a rastreabilidade ficou clara.
- **Backlog priorizado e quadro visual.** Cinco cartões pequenos deixaram o progresso e o que faltava evidentes.
- **Testes com API simulada.** Rodam offline e em milissegundos (54 testes em cerca de 0,08 s), o que dá feedback rápido.

## O que a sprint ensinou
- A **revisão (Sprint Review/inspeção)** compensou: ela encontrou um erro 500 com valores gigantes e uma validação frouxa (`1_000`), que os testes iniciais não cobriam. Isso mostra que testes bons vêm de olhar para os casos extremos, não só para o caminho feliz.
- Uma **inconsistência no requisito** (pedia "login" em vez de "conversor") foi resolvida perguntando ao Product Owner antes de começar, em vez de assumir. Esclarecer cedo evita retrabalho.
- A **Definição de Pronto** evitou marcar como concluído algo apenas "escrito": só vale com testes verdes, documentação e revisão.

## O que melhorar (Retrospectiva)
- Aplicar TDD: escrever os testes de casos extremos antes do código.
- Estimar os cartões (ex.: pontos ou horas) para comparar planejado e realizado.
- Incluir cache das taxas e mais moedas na próxima sprint (ver `docs/revisao.md`).
- Automatizar a execução dos testes com CI a cada commit.

## Papéis nesta atividade (individual)
Como a atividade é individual, uma pessoa acumulou Product Owner (priorizar e definir critérios), Developer (código e testes) e Scrum Master (manter o quadro e remover impedimentos). Em um time real esses papéis são separados, e essa separação é justamente o que dá independência à priorização e à revisão.
