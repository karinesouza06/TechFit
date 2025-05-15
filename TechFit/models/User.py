from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import obter_conexao 
class User(UserMixin):
    id : str
    def __init__(self, id, nome, email, senha, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho, idade, peso, altura, foco_treino, tipo_treino, contador = 0):
        self.id = id 
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.tipo_usuario = tipo_usuario
        self.dias_treino = dias_treino
        self.horario_treino = horario_treino
        self.dias_trabalho = dias_trabalho
        self.horario_trabalho = horario_trabalho
        self.idade = idade 
        self.peso = peso   
        self.altura = altura 
        self.foco_treino = foco_treino 
        self.tipo_treino = tipo_treino
        self.contador = contador
    
    def get_id(self):
        return self.id
        
    @classmethod
    def get(cls, user_id):
        conn = obter_conexao()
        user = conn.execute("SELECT * FROM users WHERE use_id = ?", (user_id,)).fetchone()
        conn.close()
        if user:
            loaduser = cls(
                id=user['use_id'], 
                email=user['use_email'], 
                senha=user['use_senha'], 
                nome=user['use_nome'], 
                telefone=user['use_telefone'], 
                data_nascimento=user['use_data_nascimento'], 
                genero=user['use_genero'], 
                tipo_usuario=user['use_tipo_usuario'], 
                dias_treino=user['use_dias_treino'], 
                horario_treino=user['use_horario_treino'], 
                dias_trabalho=user['use_dias_trabalho'], 
                horario_trabalho=user['use_horario_trabalho'],
                idade=user['use_idade'],
                peso=user['use_peso'],
                altura=user['use_altura'],
                foco_treino=user['use_foco_treino'],
                tipo_treino=user['use_tipo_treino'],
                contador=user['use_contador'])
        
            return loaduser
        else:
            return None


    @classmethod
    def get_by_email(cls, email):
        conn = obter_conexao()
        user = conn.execute("SELECT * FROM users WHERE use_email = ?", (email,)).fetchone()
        conn.close()
        if user:
            return cls(
                id=user['use_id'], 
                nome=user['use_nome'], 
                email=user['use_email'], 
                senha=user['use_senha'], 
                telefone=user['use_telefone'], 
                data_nascimento=user['use_data_nascimento'], 
                genero=user['use_genero'], 
                tipo_usuario=user['use_tipo_usuario'], 
                dias_treino=user['use_dias_treino'], 
                horario_treino=user['use_horario_treino'], 
                dias_trabalho=user['use_dias_trabalho'], 
                horario_trabalho=user['use_horario_trabalho'],
                idade=user['use_idade'],
                peso=user['use_peso'],
                altura=user['use_altura'],
                foco_treino=user['use_foco_treino'],
                tipo_treino=user['use_tipo_treino']
            )
        return None

    @classmethod
    def exists(cls, email):
        conn = obter_conexao()
        user = conn.execute("SELECT * FROM users WHERE use_email = ?", (email,)).fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
        
    
    @classmethod
    def inserir_users(cls, nome, senha, email, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho):
        conn = obter_conexao()
        hash_senha = generate_password_hash(senha)
        conn.execute(
            'INSERT INTO users (use_nome, use_email,use_senha, use_telefone, use_data_nascimento, use_genero, use_tipo_usuario, use_dias_treino, use_horario_treino, use_dias_trabalho, use_horario_trabalho) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (nome, email, hash_senha, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho)
        )
        conn.commit()

        user_id = conn.execute("SELECT use_id FROM users WHERE use_nome = ? AND use_email = ? ", (nome, email)).fetchone()
        conn.close()
        return user_id[0]

    @classmethod
    def atualizar_dados(cls, nome, email, telefone, data_nascimento, idade, peso, altura, foco_treino, id):
        conn = obter_conexao()
        conn.execute(
            'UPDATE users SET use_nome = ?, use_email = ?, use_telefone = ?, use_data_nascimento = ?, use_idade = ?, use_peso = ?, use_altura = ?, use_foco_treino = ? WHERE use_id = ?',
            (nome, email, telefone, data_nascimento, idade, peso, altura, foco_treino, id)
        )
        conn.commit()

    @classmethod
    def atualizar_dados_personal(cls, nome, email, telefone, data_nascimento, idade, peso, altura, 
                            formacao, cursos, tempo_trabalho, tipo_aluno, ambiente_trabalho, id):
        conn = obter_conexao()
        try:
            # Update basic user data
            conn.execute(
                'UPDATE users SET use_nome = ?, use_email = ?, use_telefone = ?, '
                'use_data_nascimento = ?, use_idade = ?, use_peso = ?, use_altura = ? '
                'WHERE use_id = ?',
                (nome, email, telefone, data_nascimento, idade, peso, altura, id)
            )
            
            # Check if personal data exists
            existing_data = conn.execute(
                "SELECT 1 FROM dados_users_personais WHERE dau_per_use_id = ?",
                (id,)
            ).fetchone()
            
            if existing_data:
                # Update existing data
                conn.execute(
                    'UPDATE dados_users_personais SET dau_per_formacao = ?, dau_per_cursos = ?, '
                    'dau_per_tempo_trabalho = ?, dau_per_tipo_aluno = ?, dau_per_ambiente_trabalho = ? '
                    'WHERE dau_per_use_id = ?',
                    (formacao, cursos, tempo_trabalho, tipo_aluno, ambiente_trabalho, id)
                )
            else:
                # Insert new data
                conn.execute(
                    'INSERT INTO dados_users_personais (dau_per_formacao, dau_per_cursos, '
                    'dau_per_tempo_trabalho, dau_per_tipo_aluno, dau_per_ambiente_trabalho, dau_per_use_id) '
                    'VALUES (?, ?, ?, ?, ?, ?)',
                    (formacao, cursos, tempo_trabalho, tipo_aluno, ambiente_trabalho, id)
                )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar dados do personal: {str(e)}")
            return False
        finally:
            conn.close()

    @classmethod
    def one(cls, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE use_id = ?', (id,))
        consultar_user = cursor.fetchone()
        conn.close()
        return consultar_user
        
    @classmethod
    def atualizar_contador(cls, user_id):
        conn = obter_conexao()
        conn.execute('UPDATE users SET use_contador = use_contador + 1 WHERE use_id = ?', (user_id,))
        conn.commit()
        conn.close()

    @classmethod
    def registrar_consumo_agua(cls, user_id, quantidade):
        conn = obter_conexao()
        try:
            conn.execute('''
                INSERT INTO consumo_agua (user_id, quantidade) 
                VALUES (?, ?)
                ON CONFLICT(user_id, data) DO UPDATE SET 
                quantidade = quantidade + excluded.quantidade
            ''', (user_id, quantidade))
            conn.commit()
        except Exception as e:
            print(f"Erro ao registrar consumo de água: {e}")
        finally:
            conn.close()

    @classmethod
    def obter_consumo_diario(cls, user_id):
        conn = obter_conexao()
        try:
            consumo = conn.execute('''
                SELECT quantidade FROM consumo_agua 
                WHERE user_id = ? AND data = CURRENT_DATE
            ''', (user_id,)).fetchone()
            return consumo[0] if consumo else 0.0
        except Exception as e:
            print(f"Erro ao obter consumo de água: {e}")
            return 0.0
        finally:
            conn.close()
