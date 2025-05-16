from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.User import User
from models import User, obter_conexao

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
            
            if user.tipo_usuario.lower() == 'aluno':
                return redirect(url_for('profile.profile'))
            elif user.tipo_usuario.lower() == 'admin':
                return redirect(url_for('auth.admin'))
            else:
                return redirect(url_for('profile.configuracoes_personal'))
            
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



@auth_bp.route('/admin')
@login_required
def admin():
    if current_user.tipo_usuario.lower() != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    return render_template('profile_admin.html', user_info=current_user)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/visualizar_alunos')
@login_required
def visualizar_alunos():
    conn = obter_conexao()
    alunos = conn.execute('''
        SELECT use_id, use_nome, use_email, use_telefone,  use_horario_treino, use_dias_treino
        FROM users
        WHERE use_tipo_usuario = 'aluno'
    ''').fetchall()
    conn.close()
    return render_template('visualizar_alunos.html', alunos=alunos)


@auth_bp.route('/personais')
def visualizar_personais():
    conn = obter_conexao()
    personais = conn.execute('''
        SELECT 
            u.use_id, u.use_nome, u.use_email, u.use_telefone,
            d.dau_per_formacao, d.dau_per_cursos, 
            d.dau_per_tempo_trabalho, d.dau_per_tipo_aluno,
            d.dau_per_ambiente_trabalho
        FROM users u
        LEFT JOIN dados_users_personais d 
        ON u.use_id = d.dau_per_use_id
        WHERE u.use_tipo_usuario = 'personal'
    ''').fetchall()
    conn.close()
    return render_template('visualizar_personais.html', personais=personais)