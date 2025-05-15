from . import obter_conexao
from models import obter_conexao

class Exercise:
    id: str
    def __init__(self, id, nome, nivel, link):
        self.id = id
        self.nome = nome
        self.nivel = nivel
        self.link = link
        

    def get_id(self):
        return self.id

    @classmethod
    def inserir_exercicio(cls, nome, nivel, link):
        conn = obter_conexao()
        conn.execute(
            'INSERT INTO exercicios (exe_nome, exe_nivel, exe_link) VALUES (?, ?, ?)',
            (nome, nivel, link)
        )
        conn.commit()
        conn.close()

    @classmethod
    def obter_exercicios(cls):
        conn = obter_conexao()
        exercicios = conn.execute('SELECT * FROM exercicios').fetchall()
        conn.close()
        return exercicios
