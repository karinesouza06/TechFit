
from flask import Flask, url_for, render_template, redirect, request
import sqlite3

app = Flask(__name__)

def obter_conexao_banco():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('inicial.html')


#como é um modal, a rota não vai funcionar, então tem que vê uma solução para isso. mas a função vai ser nesse modelo.
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'GET':
        return render_template ('cadastro.html')
    
    else:
        nome = request.form['nome']
        senha = request.form['senha']


        conn = obter_conexao_banco()
        usuario = conn.execute('SELECT * FROM dados_usuarios WHERE nome = (?) AND senha = (?)' , (nome, senha,)).fetchone()
        conn.commit()

        if usuario:
            if senha == usuario['senha']:
                return redirect(url_for('calcular_agua'))  #COLOQUEI PARA REDIRECIONAR PARA ESSA "PÁGINA" ENQUANTO AINDA NÃO TEMOS A DO ALUNO/PERSONAL
        
        else:
            return redirect(url_for('cadastro'))



@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():

    if request.method == 'GET':
        return render_template ('cadastro.html')
    
    else:
        nome = request.form['nome']
        senha = request.form['senha']
        confirmasenha = request.form['confirmasenha']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nascimento = request.form['data']
        tipo_usuario = request.form['user-type']
        genero = request.form['genero']
        dias_treino = request.form['dias_treino']
        horario_treino = request.form['horario_treino']
        dias_trabalho = request.form['dias_trabalho']
        horario_trabalho = request.form['horario_trabalho']


        conn = obter_conexao_banco()
        usuario = conn.execute('SELECT * FROM dados_usuarios WHERE nome = (?) AND email = (?)', (nome, email,)).fetchone()
        conn.commit()
 
        if usuario:
            return render_template('inicial.html') #REDIRECIONA PARA A INICIAL PARA O USUÁRIO FAZER LOGIN.
        
        else:
            if senha == confirmasenha:
                conn.execute('INSERT INTO dados_usuarios (nome, senha, email, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (nome, senha, email, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho,)).fetchone()
                conn.commit()
                conn.close() 
        
                return render_template('inicial.html')
            
        return render_template('cadastro.html')
        
@app.route('/dado_aluno')
def dado_aluno():
    return render_template('form_aluno.html')

@app.route('/inserir_medidas')
def inserir_medidas():
    return render_template('inserir_medidas.html')

@app.route('/calcular_imc')
def calcular_imc():
    return render_template('calculo_imc.html')

@app.route('/calcular_agua')
def calcular_agua():
    return render_template('calculo_agua.html')
