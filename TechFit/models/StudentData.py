from . import obter_conexao
from models import obter_conexao

class DadosUserAluno:
    id : str
    def __init__(self, id, quadril, peitoral, ombro, cintura, gluteos, dorsal, bic_esquerdo, bic_direito, coxa_esquerda, coxa_direita, pan_esquerda, pan_direita):
        self.id = id 
        self.quadril = quadril
        self.peitoral = peitoral
        self.ombro = ombro
        self.cintura = cintura
        self.gluteos = gluteos
        self.dorsal = dorsal
        self.bic_esquerdo = bic_esquerdo
        self.bic_direito = bic_direito
        self.coxa_esquerda = coxa_esquerda
        self.coxa_direita = coxa_direita
        self.pan_esquerda = pan_esquerda
        self.pan_direita = pan_direita

    def get_id(self):
        return self.id
    
    @classmethod
    def inserir_dados(cls, id,
              quadril, peitoral, ombro, cintura, gluteos, dorsal, 
              bic_esquerdo, bic_direito, 
              coxa_esquerda, coxa_direita, 
              pan_esquerda, pan_direita):
        
        conn = obter_conexao()
        sql = """INSERT INTO dados_users_alunos (
                dau_alu_quadril, dau_alu_peitoral, dau_alu_ombro, dau_alu_cintura, dau_alu_gluteos, dau_alu_dorsal,
                dau_alu_biceps_esquerdo, dau_alu_biceps_direito,
                dau_alu_coxa_esquerda, dau_alu_coxa_direita,
                dau_alu_panturrilha_esquerda, dau_alu_panturrilha_direita,
                dau_alu_use_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)  """
        
        params = (
            quadril, peitoral, ombro, cintura, gluteos, dorsal,
            bic_esquerdo, bic_direito,
            coxa_esquerda, coxa_direita,
            pan_esquerda, pan_direita,
            id  
        )
        
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()

    @classmethod
    def obter_dado_aluno(cls):
        conn = obter_conexao()
        dados_aluno = conn.execute('SELECT * FROM dados_users_alunos').fetchall()
        conn.close()
        return dados_aluno