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
    if request.method == 'GET':
        return render_template ('cadastro.html')
    else:
        nome = request.form['nome']
        senha = request.form['senha']
        confirmasenha = request.form['confirmasenha']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nascimento = request.form['data']
        tipo_usuario = request.form['tipoUsuario']
        genero = request.form['genero']
        dias_treino = request.form['dias_treino']
        horario_treino = request.form['horario_treino']
        dias_trabalho = request.form['dias_trabalho']
        horario_trabalho = request.form['horario_trabalho']

        if User.exists(email) == False:
            if senha == confirmasenha:
                user = User.inserir_users(nome, senha, email, telefone, data_nascimento, genero, tipo_usuario, dias_treino, horario_treino, dias_trabalho, horario_trabalho)
                login_user(user)
                flash("Cadastro realizado com sucesso")
                return redirect(url_for('login'))  # Redirecionar para a página de login
            else:
                flash("As senhas não coincidem")
        else:
            flash("Usuário já existente")
    return render_template('index.html')




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['email']
        senha = request.form['password']  
        return 'TELA DE TESTE'
    #     user = User.get_by_email(email)
    #     if check_password_hash(user['password'], password):
    #         login_user(User.get(user['id']))
    #         flash("Você está logado")
    #         return redirect(url_for('dash'))
    #     else:
    #         flash("Dados incorretos")
    #         return redirect(url_for('login'))
    # return render_template('pages/auth/login.html')
    return render_template('index.html')
             


# 8 - logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))