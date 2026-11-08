# Citizen Assist AI - Primeiro Emprego

Assistente de terminal, em Python, que orienta **jovens que estão buscando o primeiro emprego** sobre documentos, trabalho e benefícios. Ele responde só com informações de fontes oficiais, mostra de onde veio cada resposta e não coleta dados pessoais.

> Global Solution 2026.2 - Pensamento Computacional e Automação com Python (FIAP, 1CCPX)

## Integrantes

| Nome | RM |
|---|---|
| Brenno Ferreira Gomes dos Santos | 570525 |
| Eduardo Moreira Silva | 569923 |

## Público e problema

**Público:** jovens de 14 a 24 anos que vão tirar os primeiros documentos ou procurar o primeiro emprego, estágio ou vaga de Jovem Aprendiz.

**Problema:** quem está começando a trabalhar não sabe por onde começar. Precisa tirar CPF, RG, título e carteira de trabalho, descobrir o PIS e entender o que é estágio e Jovem Aprendiz. A informação está espalhada em vários sites do governo, em linguagem técnica e misturada com páginas que parecem oficiais mas não são (e às vezes cobram por serviços gratuitos).

## ODS relacionados

- **ODS 4 - Educação de qualidade:** orientação sobre Enem e isenção da taxa.
- **ODS 8 - Trabalho decente e crescimento econômico:** acesso a documentos, primeiro emprego, estágio e aprendizagem.
- **ODS 10 - Redução das desigualdades:** informação simples e gratuita para jovens de baixa renda (ex.: ID Jovem).
- **ODS 16 - Instituições eficazes:** facilita o acesso a serviços públicos e evita golpes com sites falsos.

## Como executar

Requisito: Python 3.10 ou superior. Não usa bibliotecas externas.

```bash
git clone <link-do-repositorio>
cd citizen-assist-ai
python main.py
```

## Estrutura

```
citizen-assist-ai/
├── README.md
├── main.py                 # menu principal; cria a base e o assistente
├── orientacao.py           # classe Orientacao (um registro do JSON)
├── base_conhecimento.py    # classe BaseConhecimento (carregar, categorias, pontuar, buscar)
├── assistente.py           # classe Assistente (perguntar, navegar, registrar, indicadores, CSV)
└── data/
    ├── base_conhecimento.json   # 12 orientações, 3 categorias
    ├── historico.json           # atendimentos registrados + notas de facilidade
    └── atendimentos.csv         # exportação dos atendimentos
```

### Classes e composição

```
Assistente
 └── base: BaseConhecimento
      └── orientacoes: [Orientacao, Orientacao, ...]
```

| Classe | Atributos | Métodos |
|---|---|---|
| `Orientacao` | id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em | `exibir()`, `de_dicionario()` |
| `BaseConhecimento` | caminho, orientacoes | `carregar()`, `categorias()`, `por_categoria()`, `pontuar()`, `buscar()`, `buscar_por_id()` |
| `Assistente` | nome, base, historico, notas | `perguntar()`, `navegar()`, `registrar()`, `indicadores()`, `exportar_csv()`, `pedir_nota()` |

## Regra de pontuação

A pergunta, as palavras-chave e o título são comparados depois de `normalizar()`: tudo em minúsculas, sem acentos e sem pontuação. Além dos sinais pedidos no enunciado, também removemos `-` e `/`, para que "meia-entrada" e "meia entrada" sejam iguais.

| Regra | Pontos |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |

| Melhor pontuação | Resultado |
|---|---|
| 6 ou mais | Confiança **ALTA** |
| 3 a 5 | Confiança **MÉDIA** |
| Menos de 3 | "Não encontrei": sugere outras palavras e as categorias |

`buscar()` devolve uma lista de **tuplas `(pontos, orientacao)`** ordenada da maior para a menor. O assistente mostra a melhor e até duas alternativas que também tenham confiança mínima.

**Exemplo:** "Como faço meu primeiro título de eleitor?"
- palavras-chave encontradas: `titulo` (+3), `titulo de eleitor` (+3), `primeiro titulo` (+3), `eleitor` (+3) = 12
- palavras do título: `primeiro` (+1), `titulo` (+1), `eleitor` (+1) = 3
- **Total: 15 pontos → confiança ALTA**

## Regras de atendimento

- **Dados pessoais:** perguntas com 8 ou mais dígitos ou com `@` são recusadas e **não são registradas**. O assistente nunca pede nome, CPF, telefone ou e-mail.
- **Entradas inválidas:** letras no lugar de números, opção fora da faixa, resposta vazia e s/n inválido mostram uma mensagem e pedem de novo, sem encerrar o programa.
- **Transparência:** toda resposta mostra a fonte, a data de verificação e o aviso de que o assistente não é canal oficial.
- **Arquivos:** JSON ausente ou corrompido mostra uma mensagem de erro em vez de travar. Registros incompletos são ignorados com aviso.

## Histórico, indicadores e CSV

Cada atendimento é salvo em `data/historico.json` com: data, origem (pergunta ou categoria), pergunta, id da orientação, se encontrou, se ajudou, tentativas e tempo em segundos (`round(time.time() - inicio, 1)`). Ao sair, o assistente pede uma nota de facilidade de 1 a 5.

Indicadores calculados (menu, opção 3): resposta encontrada (%), taxa de acerto (%), tempo médio para encontrar, tentativas por atendimento, facilidade média e lista de dúvidas sem solução. A opção 4 exporta tudo para `data/atendimentos.csv` com `csv.DictWriter`.

## Integrações com outras disciplinas

O mesmo tema (serviços e orientações ao cidadão) foi usado em **Data Structures and Algorithms**, em que os serviços são guardados em uma lista encadeada. Neste projeto, a busca por pontuação é a obrigatória de PCP.

## Fontes consultadas (verificadas em 08/11/2026)

- Receita Federal - Inscrever no CPF: https://www.gov.br/pt-br/servicos/inscrever-no-cpf
- Carteira de Identidade Nacional: https://www.gov.br/governodigital/pt-br/identidade
- TSE - Autoatendimento Eleitoral: https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral
- Exército Brasileiro - Alistamento: https://alistamento.eb.mil.br
- Conta gov.br: https://www.gov.br/governodigital/pt-br/conta-gov-br
- Carteira de Trabalho Digital: https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho
- Lei da Aprendizagem (Lei 10.097/2000): https://www.planalto.gov.br/ccivil_03/leis/l10097.htm
- Lei do Estágio (Lei 11.788/2008): https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11788.htm
- Emprega Brasil / Sine: https://empregabrasil.mte.gov.br
- ID Jovem: https://idjovem.juventude.gov.br
- Inep - Enem: https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/enem

## Resultado do teste com usuários

Testamos com **[X] pessoas de fora da equipe**, em **[X] atendimentos**. Não registramos nomes nem dados dos participantes.

| Indicador | Resultado |
|---|---|
| Resposta encontrada | [X]% |
| Taxa de acerto (ajudou) | [X]% |
| Tempo médio para encontrar | [X] s |
| Tentativas por atendimento | [X] |
| Facilidade de uso (1 a 5) | [X] |

**Dúvidas sem solução:**
- [copiar da opção 3 do menu]

**Melhoria feita a partir do teste:** [ex.: a pergunta "quero viajar de graça de ônibus" não era encontrada. Incluímos a palavra-chave "viajar de graca" na orientação da ID Jovem e ela passou a ser respondida.]

## Limitações

- A busca é por palavras: se a pessoa usar sinônimos que não estão nas palavras-chave ou escrever com erro de digitação, a orientação não é encontrada.
- Não entende frases negativas nem contexto (ex.: "não quero CPF" também pontua para CPF).
- As informações precisam ser conferidas e atualizadas manualmente, porque regras e sites do governo mudam.
- O bloqueio de dados pessoais usa regras simples (dígitos e `@`). Um nome completo, por exemplo, não é detectado.

## Vídeo técnico

[link do YouTube (não listado)]
