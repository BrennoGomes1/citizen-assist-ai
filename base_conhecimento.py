"""Classe BaseConhecimento: lê o JSON e faz a busca por pontuação."""

import json

from orientacao import Orientacao

CAMPOS_OBRIGATORIOS = ("id", "categoria", "titulo", "palavras_chave", "resposta",
                       "documentos", "onde", "fonte", "verificado_em")

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Pesos e limites da pontuação (explicados no README)
PONTOS_PALAVRA_CHAVE = 3
PONTOS_PALAVRA_TITULO = 1
TAMANHO_MINIMO_PALAVRA = 4
LIMITE_ALTA = 6
LIMITE_MEDIA = 3


def normalizar(texto):
    """Minúsculas, sem acentos, sem pontuação e com espaços nas pontas."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()-/":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def nivel_confianca(pontos):
    """Converte a pontuação em ALTA, MÉDIA ou None (não encontrado)."""
    if pontos >= LIMITE_ALTA:
        return "ALTA"
    if pontos >= LIMITE_MEDIA:
        return "MÉDIA"
    return None


class BaseConhecimento:
    """Conjunto de todas as orientações (composição: lista de Orientacao)."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao. Retorna True se deu certo."""
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido (JSON inválido).")
            return False

        if not isinstance(dados, list):
            print("Erro: a base de conhecimento deve ser uma lista de orientações.")
            return False

        self.orientacoes = []
        for registro in dados:
            if isinstance(registro, dict) and all(c in registro for c in CAMPOS_OBRIGATORIOS):
                self.orientacoes.append(Orientacao.de_dicionario(registro))
            else:
                print("Aviso: um registro incompleto da base foi ignorado.")
        return len(self.orientacoes) > 0

    def categorias(self):
        """Lista as categorias sem repetição, na ordem em que aparecem."""
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        """Retorna as orientações de uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    def buscar_por_id(self, id_orientacao):
        for orientacao in self.orientacoes:
            if orientacao.id == id_orientacao:
                return orientacao
        return None

    def pontuar(self, pergunta_normalizada, orientacao):
        """Calcula os pontos de uma orientação para a pergunta.

        +3 para cada palavra-chave que aparece na pergunta;
        +1 para cada palavra da pergunta (4+ letras) que aparece no título.
        """
        pontos = 0
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_normalizada:
                pontos += PONTOS_PALAVRA_CHAVE

        palavras_titulo = normalizar(orientacao.titulo).split()
        for palavra in set(pergunta_normalizada.split()):
            if len(palavra) >= TAMANHO_MINIMO_PALAVRA and palavra in palavras_titulo:
                pontos += PONTOS_PALAVRA_TITULO
        return pontos

    def buscar(self, pergunta):
        """Retorna uma lista de tuplas (pontos, orientacao), da maior para a menor."""
        pergunta_normalizada = normalizar(pergunta)
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta_normalizada, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados
