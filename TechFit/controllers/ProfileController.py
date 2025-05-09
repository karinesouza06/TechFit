from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from models.User import User
from models import User, Treino
from models import obter_conexao 
from flask import jsonify


profile_bp = Blueprint('profile', __name__)

# DADOS DOS ALUNOS
@profile_bp.route('/profile')
@login_required
def profile():
    user_id = current_user.get_id()
    user = User.get(user_id)
    total_treinos = Treino.contar_treinos(user_id)
    
    if user:
        user.total_treinos = total_treinos
        return render_template('profile.html', user_info=user)
    else:
        flash("Usuário não encontrado.")
        return redirect(url_for('index'))
    
@profile_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    userid = current_user.get_id()
    user = User.get(userid)
    
    if request.method == 'POST':
        nome = request.form['nome_edit']
        email = request.form['email_edit']
        telefone = request.form['telefone_edit']
        data_nascimento = request.form['data_nascimento_edit']
        idade = request.form['idade_edit']
        peso = request.form['peso_edit']
        altura = request.form['altura_edit']
        foco_treino = request.form['foco_treino_edit']
                
        User.atualizar_dados(nome, email, telefone, data_nascimento, idade, peso, altura, foco_treino, userid)
        
    um_user = User.one(userid)
    return render_template('configuracoes.html', user=um_user, user_info=user)



@profile_bp.route('/solicitar_personal/<int:personal_id>', methods=['POST'])
@login_required
def solicitar_personal(personal_id):
    # Lógica para registrar a solicitação
    return jsonify({'success': True})


# @profile_bp.route('/seleciona_personal', methods=['GET', 'POST'])
# @login_required
# def seleciona_personal():
#     conn = obter_conexao()
#     personais = conn.execute('''
#         SELECT u.use_id, u.use_nome, u.use_email, u.use_telefone,
#                d.dau_per_formacao, d.dau_per_cursos, d.dau_per_tempo_trabalho,
#                d.dau_per_tipo_aluno, d.dau_per_ambiente_trabalho
#         FROM users u
#         LEFT JOIN dados_users_personais d ON u.use_id = d.dau_per_use_id
#         WHERE u.use_tipo_usuario = 'personal'
#     ''').fetchall()
#     conn.close()
#     return render_template('selecionar_personal.html', personais=personais)

@profile_bp.route('/seleciona_personal', methods=['GET', 'POST'])
@login_required
def seleciona_personal():
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
    return render_template('selecionar_personal.html', personais=personais)


#DADOS DOS PERSONAIS
@profile_bp.route('/profile_personal')
@login_required
def profile_personal():
    user_id = current_user.get_id()
    user = User.get(user_id)
    
    return render_template('profile_personal.html', user_info=user)


@profile_bp.route('/configuracoes_personal', methods=['GET', 'POST'])
@login_required
def configuracoes_personal():
    userid = current_user.get_id()
    user = User.get(userid)
    
    if request.method == 'POST':
        nome = request.form['nome_edit']
        email = request.form['email_edit']
        telefone = request.form['telefone_edit']
        data_nascimento = request.form['data_nascimento_edit']
        idade = request.form['idade_edit']
        peso = request.form['peso_edit']
        altura = request.form['altura_edit']
        foco_treino = request.form['foco_treino_edit']
                
        User.atualizar_dados(nome, email, telefone, data_nascimento, idade, peso, altura, foco_treino, userid)
        
    um_user = User.one(userid)
    return render_template('configuracoes_personal.html', user=um_user, user_info=user)

@profile_bp.route('/seleciona_aluno', methods=['GET', 'POST'])
@login_required
def seleciona_aluno():
    return render_template('selecionar_aluno.html')

