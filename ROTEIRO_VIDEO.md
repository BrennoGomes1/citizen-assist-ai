# Roteiro do vídeo técnico - PCP (5 a 8 minutos)

Regras: os dois falam, cada um explica uma parte técnica; tela com o código legível (aumente a fonte do VS Code com Ctrl + +); nada de voz de IA. Fale com as suas palavras, este roteiro é só um guia.

Antes de gravar: zere o histórico (`data/historico.json` com `{"atendimentos": [], "notas_facilidade": []}`) **só depois** de anotar os indicadores do teste com usuários, ou grave a parte 7 primeiro.

---

## 1. Equipe, público e problema - BRENNO (até 30 s)
*Tela: README aberto.*

"Somos Brenno Santos e Eduardo Moreira. Nosso assistente é para jovens que estão buscando o primeiro emprego. Quem está começando não sabe como tirar CPF, título, carteira de trabalho ou o que é Jovem Aprendiz. A informação está espalhada e tem muito site falso cobrando por serviço gratuito."

## 2. JSON, dicionários e tuplas - BRENNO (~1 min)
*Tela: `data/base_conhecimento.json`, registro de id 1 (CPF).*

- "A base é uma lista de dicionários. Cada dicionário é uma orientação."
- Mostre campo por campo: id, categoria, título, palavras_chave (uma lista), resposta, documentos, onde, fonte e verificado_em.
- "Temos 14 orientações em 3 categorias: Documentos, Trabalho, e Educação e Benefícios. Todas com fonte oficial e data de verificação."
- "As tuplas aparecem na busca: cada resultado é uma tupla com pontos e a orientação."

## 3. Classes, self e composição - EDUARDO (~1 min 30)
*Tela: `orientacao.py`, depois `base_conhecimento.py`, depois `assistente.py`.*

- `Orientacao`: "O `__init__` recebe os campos e guarda com `self`, que é o próprio objeto. O `exibir()` mostra a resposta com fonte e aviso."
- `BaseConhecimento`: "Tem o caminho do arquivo e a lista de objetos Orientacao. O `carregar()` lê o JSON com try/except: se o arquivo não existe ou está corrompido, mostra mensagem e não trava."
- `Assistente`: "Tem um atributo `base`, que é um objeto BaseConhecimento. Isso é composição: o assistente tem uma base, e a base tem várias orientações."
- Mostre no `main.py` como os objetos são criados.

## 4. Busca: normalizar() e pontuar() - BRENNO (~1 min 30)
*Tela: `base_conhecimento.py`, funções `normalizar` e `pontuar`.*

- "O `normalizar()` deixa tudo minúsculo, tira acentos e pontuação, e coloca espaço nas pontas. Assim, 'Título' e 'titulo' ficam iguais, e o espaço evita achar 'sus' dentro de outra palavra."
- "No `pontuar()`, cada palavra-chave que aparece na pergunta vale 3 pontos, e cada palavra da pergunta com 4 letras ou mais que está no título vale 1."
- **Cálculo de exemplo:** "Como faço meu primeiro título de eleitor?" → palavras-chave titulo, titulo de eleitor, primeiro titulo e eleitor: 4 × 3 = 12; palavras do título primeiro, titulo e eleitor: +3. Total 15, confiança ALTA (6 ou mais é alta, 3 a 5 é média, menos de 3 não encontrou).
- "O `buscar()` devolve uma lista de tuplas (pontos, orientação) ordenada da maior para a menor."

## 5. Execução - EDUARDO (~1 min 30)
*Tela: terminal, `python main.py`.*

1. Opção 1 → "Como faço meu primeiro título de eleitor?" → mostre a confiança ALTA, a fonte e o aviso → responda `s`.
2. "Como faço o cartão do SUS?" → **não encontrada** (não é do nosso público) → mostra sugestões.
3. Digite `x` quando pedir s/n → **entrada inválida**, o programa não fecha.
4. "meu cpf é 123.456.789-00" → **dado pessoal bloqueado**, não é registrado.
5. `0` para voltar, opção 2 → **categorias** → Trabalho → Ser Jovem Aprendiz → `0` para voltar. Digite `9` em um menu para mostrar "opção fora da faixa".

## 6. Alteração ao vivo - BRENNO (~1 min)
1. No terminal, pergunte "quero viajar de graça de ônibus" → **não encontrei**.
2. Saia, abra o JSON, vá na orientação 11 (ID Jovem) e adicione `"viajar de graca"` em `palavras_chave`. Salve.
3. Rode de novo e faça a mesma pergunta → agora aparece a ID Jovem com confiança MÉDIA (3 pontos).
4. "A pergunta não tinha nenhuma palavra-chave. Com a nova, ganhou 3 pontos e passou a ser encontrada."

## 7. Histórico, CSV e indicadores - EDUARDO (~1 min)
- Abra `data/historico.json`: "cada atendimento é um dicionário com data, origem, pergunta, id, se encontrou, se ajudou, tentativas e tempo."
- No menu, opção 4 → abra `data/atendimentos.csv`: "exportado com `csv.DictWriter`."
- Opção 3 → mostre os **indicadores do teste com as [X] pessoas**: % encontrada, % de acerto, tempo médio, tentativas, nota de facilidade e dúvidas sem solução.

## 8. Decisão técnica e limitação - BRENNO e EDUARDO (~30 s)
- **Brenno (decisão técnica):** "Não registramos perguntas com dado pessoal, nem no histórico. Assim, o sistema nunca guarda um CPF por engano."
- **Eduardo (limitação):** "A busca é por palavras. Se a pessoa usar um sinônimo que não está na base ou digitar errado, não encontramos. Uma melhoria seria corrigir erros de digitação."
