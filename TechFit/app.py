from flask import Flask, url_for, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


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
    return render_template('inserir_medidas.html')

@app.route('/calcular_imc')
def calcular_imc():
    return render_template('calculo_imc.html')

@app.route('/calcular_agua')
def calcular_agua():
    return render_template('calculo_agua.html')
