from . import obter_conexao
from models import obter_conexao

class Treino:
    @classmethod
    def registrar_treino(cls, user_id, data_treino):
        conn = obter_conexao()
        conn.execute(
            'INSERT INTO dias_treino (user_id, data_treino) VALUES (?, ?)',
            (user_id, data_treino)
        )
        conn.commit()
        conn.close()

    @classmethod
    def contar_treinos(cls, user_id):
        conn = obter_conexao()
        count = conn.execute(
            'SELECT COUNT(*) FROM dias_treino WHERE user_id = ?',
            (user_id,)
        ).fetchone()[0]
        conn.close()
        return count
    
    @classmethod
    def obter_treinos(cls, user_id):
        conn = obter_conexao()
        treinos = conn.execute(
            'SELECT data_treino FROM dias_treino WHERE user_id = ?',
            (user_id,)
        ).fetchall()
        conn.close()
        return [{'data_treino': treino['data_treino']} for treino in treinos]
