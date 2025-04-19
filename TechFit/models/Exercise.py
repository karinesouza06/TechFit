from . import obter_conexao
from models import obter_conexao

class Exercise:
    id: str
    def __init__(self, id, nome, link, tipo, nivel):
        self.id = id
        self.nome = nome
        self.link = link
        self.tipo = tipo
        self.nivel = nivel

    @classmethod
    def inserir_exercicio(cls, nome, link, tipo, nivel):
        conn = obter_conexao()
        conn.execute(
            'INSERT INTO exercicios VALUES (?, ?, ?, ?)',
            (nome, link, tipo, nivel)
        )
        conn.commit()
        conn.close()

    @classmethod
    def obter_exercicios(cls):
        conn = obter_conexao()
        exercicios = conn.execute('SELECT * FROM exercicios').fetchall()
        conn.close()
        return exercicios