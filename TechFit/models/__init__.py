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
    def __init__(self, nome, email, senha, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho):
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
        
    @classmethod
    def get(cls,user_id):
        conn = obter_conexao()
        user = conn.execute("SELECT * FROM users WHERE use_id = ?", (user_id,)).fetchone()
        conn.close()
        if user:
            loaduser = User(email=user['email'] , senha=user['senha'])
            loaduser.id = user['id']
            return loaduser
        else:
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
            'INSERT INTO users  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (nome, email, hash_senha, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho)
        )
        conn.commit()
        conn.close()

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
            
        
        