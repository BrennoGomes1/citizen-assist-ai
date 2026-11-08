"""Classe Assistente: conversa com o cidadão, guarda o histórico e calcula indicadores."""

import csv
import json
import time
from datetime import datetime

from base_conhecimento import nivel_confianca

CAMPOS_HISTORICO = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                    "ajudou", "tentativas", "tempo_segundos"]


def contem_dado_pessoal(texto):
    """Pergunta com 8 ou mais dígitos (CPF, telefone) ou com @ (e-mail)."""
    digitos = sum(1 for caractere in texto if caractere.isdigit())
    return digitos >= 8 or "@" in texto


def ler_opcao(mensagem, minimo, maximo):
    """Lê um número entre minimo e maximo. Nunca encerra o programa."""
    while True:
        entrada = input(mensagem).strip()
        if entrada == "":
            print("Resposta vazia. Digite um número.")
        elif not entrada.isdigit():
            print("Opção inválida: digite apenas números.")
        elif not minimo <= int(entrada) <= maximo:
            print(f"Opção fora da faixa. Escolha de {minimo} a {maximo}.")
        else:
            return int(entrada)


def ler_sim_nao(mensagem):
    """Lê 's' ou 'n'. Repete até receber uma resposta válida."""
    while True:
        entrada = input(mensagem).strip().lower()
        if entrada in ("s", "sim"):
            return True
        if entrada in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite s para sim ou n para não.")


class Assistente:
    """Quem conversa com o cidadão. Tem uma BaseConhecimento (composição)."""

    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico = []
        self.notas = []
        self.carregar_historico()

    # ---------------- Arquivos ----------------
    def carregar_historico(self):
        """Lê o histórico salvo. Arquivo ausente ou corrompido não trava o programa."""
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.historico = dados.get("atendimentos", [])
            self.notas = dados.get("notas_facilidade", [])
        except FileNotFoundError:
            self.historico, self.notas = [], []
        except (json.JSONDecodeError, AttributeError):
            print("Aviso: histórico corrompido. Começando um histórico novo.")
            self.historico, self.notas = [], []

    def salvar_historico(self):
        dados = {"atendimentos": self.historico, "notas_facilidade": self.notas}
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    # ---------------- Atendimento ----------------
    def registrar(self, origem, pergunta, orientacao, ajudou, tentativas, inicio):
        """Salva um atendimento (dicionário) no histórico."""
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": orientacao is not None,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1),
        }
        self.historico.append(atendimento)
        self.salvar_historico()

    def perguntar(self):
        """Recebe dúvidas em texto livre e responde com a busca por pontuação."""
        tentativas = 0
        inicio = time.time()
        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if pergunta == "":
                print("Você não digitou nada. Escreva sua dúvida com suas palavras.")
                continue
            if contem_dado_pessoal(pergunta):
                # Não registra nada: a pergunta tinha dado pessoal
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)
            melhor_pontos = resultados[0][0] if resultados else 0
            confianca = nivel_confianca(melhor_pontos)

            if confianca is None:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras (ex.: 'cpf', 'carteira de trabalho', 'estágio')")
                print("ou navegue pelas categorias: " + ", ".join(self.base.categorias()))
                self.registrar("pergunta", pergunta, None, False, tentativas, inicio)
                continue

            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir()

            alternativas = [o for p, o in resultados[1:3] if nivel_confianca(p)]
            if alternativas:
                print("\nTalvez você também queira ver:")
                for orientacao in alternativas:
                    print(f"  - {orientacao.titulo}")

            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("pergunta", pergunta, melhor, ajudou, tentativas, inicio)
            if ajudou:
                tentativas = 0
                inicio = time.time()
            else:
                print("Tente explicar de outro jeito ou use o menu de categorias.")

    def navegar(self):
        """Navegação por categorias, com '0 para voltar' em todas as telas."""
        inicio = time.time()
        while True:
            categorias = self.base.categorias()
            print("\n=== Categorias ===")
            for numero, categoria in enumerate(categorias, start=1):
                print(f"{numero}. {categoria}")
            print("0. Voltar")
            escolha = ler_opcao("Escolha uma categoria: ", 0, len(categorias))
            if escolha == 0:
                return
            categoria = categorias[escolha - 1]

            while True:
                orientacoes = self.base.por_categoria(categoria)
                print(f"\n=== {categoria} ===")
                for numero, orientacao in enumerate(orientacoes, start=1):
                    print(f"{numero}. {orientacao.titulo}")
                print("0. Voltar")
                escolha = ler_opcao("Escolha uma orientação: ", 0, len(orientacoes))
                if escolha == 0:
                    break
                orientacao = orientacoes[escolha - 1]
                orientacao.exibir()
                ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", categoria, orientacao, ajudou, 1, inicio)
                inicio = time.time()

    # ---------------- Indicadores e CSV ----------------
    def indicadores(self):
        """Calcula e exibe os indicadores dos atendimentos registrados."""
        total = len(self.historico)
        print("\n=== Indicadores ===")
        if total == 0:
            print("Ainda não há atendimentos registrados.")
            return

        encontrados = [a for a in self.historico if a["encontrou"]]
        ajudaram = [a for a in self.historico if a["ajudou"]]
        tempo_medio = (sum(a["tempo_segundos"] for a in ajudaram) / len(ajudaram)
                       if ajudaram else 0)
        tentativas_media = sum(a["tentativas"] for a in self.historico) / total
        sem_solucao = [a["pergunta"] for a in self.historico
                       if a["origem"] == "pergunta" and not a["ajudou"]]

        print(f"Total de atendimentos: {total}")
        print(f"Resposta encontrada: {len(encontrados) / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {len(ajudaram) / total * 100:.1f}%")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f} s")
        print(f"Tentativas por atendimento: {tentativas_media:.1f}")
        if self.notas:
            print(f"Facilidade de uso (1 a 5): {sum(self.notas) / len(self.notas):.1f} "
                  f"({len(self.notas)} avaliações)")
        else:
            print("Facilidade de uso (1 a 5): sem avaliações ainda")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  (nenhuma)")

    def exportar_csv(self):
        """Exporta os atendimentos para CSV com csv.DictWriter."""
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_HISTORICO)
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
            print(f"{len(self.historico)} atendimentos exportados para {self.caminho_csv}.")
        except OSError:
            print("Erro: não foi possível criar o arquivo CSV.")

    def pedir_nota(self):
        """Ao sair, pede uma nota de facilidade de 1 a 5."""
        nota = ler_opcao("\nDe 1 a 5, quão fácil foi usar o assistente? ", 1, 5)
        self.notas.append(nota)
        self.salvar_historico()
        print("Obrigado pela avaliação!")
