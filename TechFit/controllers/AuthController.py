from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models.User import User
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'GET'])
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

                user = User(id=id, nome=nome, email=email, senha=senha, telefone=telefone, data_nascimento=data_nascimento, genero=genero, tipo_usuario=tipo_usuario, dias_treino=dias_treino, horario_treino=horario_treino, dias_trabalho=dias_trabalho, horario_trabalho=horario_trabalho)
                login_user(user)
               
                flash("Cadastro realizado com sucesso. Faça login agora!")
                return redirect(url_for('index')) 
            else:
                flash("As senhas não coincidem.")
        else:
            flash("Usuário já existente.")
    return render_template('index.html')
    

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_by_email(email)
        
        if user and check_password_hash(user.senha, password):
            login_user(user)
            
            if user.tipo_usuario == 'Aluno' or user.tipo_usuario == 'aluno' :
                return redirect(url_for('profile.profile'))
            else:
                return redirect(url_for('profile_personal.profile_personal'))
            
        else:
            flash('Credenciais inválidas')
            return redirect(url_for('index'))

    return redirect(url_for('auth.login'))


@auth_bp.route('/agua', methods=['POST', 'GET'])
def agua():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Usuário não autenticado'}), 401
        
    if request.method == 'POST':
        quantidade = request.json.get('quantidade')
        User.registrar_consumo_agua(current_user.id, quantidade)
        return jsonify({'success': True})
    
    if request.method == 'GET':
        total = User.obter_consumo_diario(current_user.id)
        return jsonify({'total': total})

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))