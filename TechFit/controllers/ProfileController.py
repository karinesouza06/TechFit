from flask import Blueprint, render_template, redirect, flash, url_for, request, Response
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

@profile_bp.route('/upload_imagem', methods=['POST'])
@login_required
def upload_imagem():
    if 'picture_input' not in request.files:
        flash('Nenhuma imagem enviada.')
        return redirecionar_para_perfil()

    file = request.files['picture_input']
    if file.filename == '':
        flash('Arquivo inválido.')
        return redirecionar_para_perfil()

    imagem_binaria = file.read()

    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET use_imagem = ? WHERE use_id = ?", (imagem_binaria, current_user.get_id()))
    conn.commit()
    conn.close()

    flash('Imagem atualizada com sucesso!')
    return redirecionar_para_perfil()


def redirecionar_para_perfil():
    user = User.get(current_user.get_id())
    if user and user.tipo_usuario == 'personal':
        return redirect(url_for('profile.profile_personal'))
    else:
        return redirect(url_for('profile.profile'))


@profile_bp.route('/imagem_usuario/<int:user_id>')
def imagem_usuario(user_id):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT use_imagem FROM users WHERE use_id = ?", (user_id,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0]:
        return Response(resultado[0], mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='placeholder.png'))

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
    if current_user.tipo_usuario.lower() != 'aluno':
        return jsonify({'error': 'Apenas alunos podem enviar solicitações'}), 403
    
    conn = obter_conexao()
    try:
        existe = conn.execute('''
            SELECT id FROM solicitacoes_personal 
            WHERE aluno_id = ? AND personal_id = ? AND status = 'pendente'
        ''', (current_user.id, personal_id)).fetchone()
        
        if not existe:
            conn.execute('''
                INSERT INTO solicitacoes_personal (aluno_id, personal_id)
                VALUES (?, ?)
            ''', (current_user.id, personal_id))
            conn.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Solicitação já enviada'}), 400
            
    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({'error': 'Falha no servidor'}), 500
    finally:
        conn.close()


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


@profile_bp.route('/seus_alunos', methods=['GET', 'POST'])
@login_required
def seus_alunos():
    conn = obter_conexao()
    alunos = conn.execute('''
        SELECT u.use_id, u.use_nome, u.use_email 
        FROM aluno_personal ap
        JOIN users u ON ap.aluno_id = u.use_id
        WHERE ap.personal_id = ?
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('alunos_vinculados.html', alunos=alunos)


@profile_bp.route('/montar_treino/<int:aluno_id>', methods=['GET', 'POST'])
@login_required
def montar_treino(aluno_id):
    # Verificar se o aluno está vinculado ao personal
    conn = obter_conexao()
    existe_vinculo = conn.execute('''
        SELECT * FROM aluno_personal 
        WHERE personal_id = ? AND aluno_id = ?
    ''', (current_user.id, aluno_id)).fetchone()
    conn.close()
    
    if not existe_vinculo:
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('profile.seus_alunos'))
    
    aluno = User.get(aluno_id)
    if not aluno:
        flash('Aluno não encontrado', 'error')
        return redirect(url_for('profile.seus_alunos'))
    
    return render_template('montar_treino.html', aluno=aluno)
    

@profile_bp.route('/solicitacoes_pendentes')
@login_required
def solicitacoes_pendentes():
    if current_user.tipo_usuario.lower() != 'personal':
        flash('Acesso restrito a personais')
        return redirect(url_for('profile.profile_personal'))
    
    conn = obter_conexao()
    solicitacoes = conn.execute('''
        SELECT s.id, u.use_id, u.use_nome, u.use_email, s.data_solicitacao 
        FROM solicitacoes_personal s
        JOIN users u ON s.aluno_id = u.use_id
        WHERE s.personal_id = ? AND s.status = 'pendente'
    ''', (current_user.id,)).fetchall()
    conn.close()
    
    return render_template('solicitacoes_pendentes.html', solicitacoes=solicitacoes)


@profile_bp.route('/aceitar_solicitacao/<int:solicitacao_id>')
@login_required
def aceitar_solicitacao(solicitacao_id):
    if current_user.tipo_usuario.lower() != 'personal':
        flash('Ação não permitida', 'error')
        return redirect(url_for('index'))
    
    conn = obter_conexao()
    try:
        solicitacao = conn.execute('''
            SELECT * FROM solicitacoes_personal
            WHERE id = ? AND status = 'pendente' AND personal_id = ?
        ''', (solicitacao_id, current_user.id)).fetchone()

        if not solicitacao:
            flash('Solicitação inválida', 'error')
            return redirect(url_for('profile.solicitacoes_pendentes'))

        # Verifica se já existe vínculo
        existe_vinculo = conn.execute('''
            SELECT * FROM aluno_personal
            WHERE aluno_id = ? AND personal_id = ?
        ''', (solicitacao['aluno_id'], current_user.id)).fetchone()

        if existe_vinculo:
            flash('Este aluno já está vinculado', 'warning')
            return redirect(url_for('profile.solicitacoes_pendentes'))

        conn.execute('''
            UPDATE solicitacoes_personal SET status = 'aceito'
            WHERE id = ?
        ''', (solicitacao_id,))
        
        conn.execute('''
            INSERT INTO aluno_personal (aluno_id, personal_id)
            VALUES (?, ?)
        ''', (solicitacao['aluno_id'], current_user.id))
        
        conn.commit()
        flash('Solicitação aceita com sucesso!', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f'Erro ao processar solicitação: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('profile.solicitacoes_pendentes'))

@profile_bp.route('/rejeitar_solicitacao/<int:solicitacao_id>')
@login_required
def rejeitar_solicitacao(solicitacao_id):
    conn = obter_conexao()
    conn.execute('''
        UPDATE solicitacoes_personal SET status = 'rejeitado'
        WHERE id = ? AND personal_id = ?
    ''', (solicitacao_id, current_user.id))
    conn.commit()
    conn.close()
    flash('Solicitação rejeitada.')
    return redirect(url_for('profile.solicitacoes_pendentes'))

@profile_bp.route('/get_medidas_corpo')
@login_required
def get_medidas_corpo():
    user_id = current_user.get_id()
    conn = obter_conexao()
    
    medidas = conn.execute('''
        SELECT dau_alu_quadril, dau_alu_peitoral, dau_alu_ombro, 
               dau_alu_cintura, dau_alu_gluteos, dau_alu_dorsal
        FROM dados_users_alunos
        WHERE dau_alu_use_id = ?
    ''', (user_id,)).fetchone()
    
    conn.close()
    
    if medidas:
        return jsonify({
            'quadril': medidas['dau_alu_quadril'],
            'peitoral': medidas['dau_alu_peitoral'],
            'ombro': medidas['dau_alu_ombro'],
            'cintura': medidas['dau_alu_cintura'],
            'gluteos': medidas['dau_alu_gluteos'],
            'dorsal': medidas['dau_alu_dorsal']
        })
    else:
        return jsonify({
            'quadril': 0,
            'peitoral': 0,
            'ombro': 0,
            'cintura': 0,
            'gluteos': 0,
            'dorsal': 0
        })

