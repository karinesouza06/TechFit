from . import obter_conexao
from models import obter_conexao

class Exercise:
    id: str
    def __init__(self, id, nome, link, nivel):
        self.id = id
        self.nome = nome
        self.link = link
        # self.tipo = tipo
        self.nivel = nivel

    # @classmethod
    # def inserir_exercicio(cls, nome, link, tipo, nivel):
    #     conn = obter_conexao()
    #     conn.execute(
    #         'INSERT INTO exercicios VALUES (?, ?, ?, ?)',
    #         (nome, link, tipo, nivel)
    #     )
    #     conn.commit()
    #     conn.close()

    # @staticmethod
    # def atualizar_tabela():
    #     conn = obter_conexao()
    #     # conn.execute('DROP TABLE IF EXISTS exercicios')
    #     conn.execute('''
    #         CREATE TABLE exercicios (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             nome TEXT NOT NULL,
    #             link TEXT NOT NULL,
    #             nivel TEXT NOT NULL
    #         )
    #     ''')
    #     conn.commit()
    #     conn.close()

    @classmethod
    def inserir_exercicio(cls, nome, link, nivel):
        conn = obter_conexao()
        conn.execute(
            'INSERT INTO exercicios (nome, link, nivel) VALUES (?, ?, ?)',  # Especifique as colunas
            (nome, link, nivel)
        )
        conn.commit()
        conn.close()

    @classmethod
    def obter_exercicios(cls):
        conn = obter_conexao()
        exercicios = conn.execute('SELECT * FROM exercicios').fetchall()
        conn.close()
        return exercicios