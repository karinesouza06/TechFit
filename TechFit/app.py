from flask import Flask, url_for, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicial.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html') 

@app.route('/dado_aluno')
def dado_alunos():
    return render_template('form_aluno.html')


@app.route('/inserir_medidas')
def inserir_medidas():
    return render_template('Inserir_medidas.html')