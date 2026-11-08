"""Classe Orientacao: representa um registro da base de conhecimento."""

AVISO_OFICIAL = "Aviso: este assistente NÃO é um canal oficial. Confirme sempre no site do órgão."


class Orientacao:
    """Guarda os dados de uma orientação e sabe se exibir na tela."""

    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave      # lista de strings
        self.resposta = resposta
        self.documentos = documentos              # lista de strings
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    @classmethod
    def de_dicionario(cls, dados):
        """Cria um objeto Orientacao a partir de um dicionário do JSON."""
        return cls(
            dados["id"], dados["categoria"], dados["titulo"],
            dados["palavras_chave"], dados["resposta"], dados["documentos"],
            dados["onde"], dados["fonte"], dados["verificado_em"],
        )

    def exibir(self):
        """Mostra a orientação completa, com fonte, data e aviso."""
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for doc in self.documentos:
            print(f"  - {doc}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(AVISO_OFICIAL)
