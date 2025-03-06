from flask import Flask, redirect, render_template, url_for, request, flash
from models import User
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import LoginManager, login_user, login_required, logout_user
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ULTRAMEGADIFICIL'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form.get('senha') 
        confirmasenha = request.form['confirmasenha']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nascimento = request.form['data']
        tipo_usuario = request.form['tipoUsuario']
        genero = request.form['genero']
        dias_treino = request.form.get('dias_treino')
        horario_treino = request.form['horario_treino']
        dias_trabalho = request.form.get('dias_trabalho')
        horario_trabalho = request.form['horario_trabalho']

        if User.exists(email) == False:
            if senha == confirmasenha:
                id = User.inserir_users(nome, senha, email, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho)

                user = User(id=id, nome = nome, email = email, senha = senha, telefone = telefone, data_nascimento = data_nascimento, genero = genero, tipo_usuario = tipo_usuario, dias_treino = dias_treino, horario_treino = horario_treino, dias_trabalho = dias_trabalho, horario_trabalho = horario_trabalho)
                login_user(user)
               
                flash("Cadastro realizado com sucesso")
            else:
                flash("As senhas não coincidem, mano")
        else:
            flash("Usuário já existente")
    else:
        return render_template('index.html')




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        
        if user and check_password_hash(user.senha, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Credenciais inválidas')
            return redirect(url_for('index'))
    return redirect(url_for('index'))
             
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/tela_exercicios')
def tela_exercicios():
    return render_template('tela_exercicios.html')

@app.route('/exercise_page')
def exercise_page():
    return render_template('exercise_page.html')

@app.route('/minhas_medidas')
def minhas_medidas():
    return render_template('minhas_medidas.html')

# 8 - logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
