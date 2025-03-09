from flask_login import UserMixin
from flask import Flask, redirect, render_template, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

database = 'database.db'

def obter_conexao():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    id : str
    def __init__(self, id, nome, email, senha, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho):
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
                horario_trabalho=user['use_horario_trabalho'])
        
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
                horario_trabalho=user['use_horario_trabalho']
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
    def verificar_tipo_user(cls, nome, senha):
        conn = obter_conexao()
        hash_senha = generate_password_hash(senha)
        user = conn.execute('SELECT use_tipo_usuario FROM users WHERE use_nome = ? AND use_senha = ?', (nome, hash_senha,)).fetchone()
 
        if user == 'Aluno':
            return "TELA DO ALUNO"
            
        elif user == 'Personal':
            return 'TELA DO PERSONAL'
            
        elif user == 'Administrador':
            return 'TELA DE ADMINISTRADOR'
        else:
            return 'TELA DO VISITANTE'

    @classmethod
    def atualizar_dados(cls, nome, email, telefone, data_nascimento, dias_treino, horario_treino, id):
        conn = obter_conexao()
        conn.execute(
            'UPDATE users SET use_nome = ?, use_email = ?, use_telefone = ?, use_data_nascimento = ?, use_dias_treino = ?, use_horario_treino = ? WHERE use_id = ?',
            (nome, email, telefone, data_nascimento, dias_treino, horario_treino, id)
        )
        conn.commit()

    @classmethod
    def one(cls, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE use_id = ?', (id,))
        consultar_user = cursor.fetchone()
        conn.close()
        return consultar_user

    
        
