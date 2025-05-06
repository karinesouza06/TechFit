from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from models.User import User
from models import User, Treino

profile_personal_bp = Blueprint('profile_personal', __name__)

@profile_personal_bp.route('/profile_personal')
@login_required
def profile_personal():
    user_id = current_user.get_id()
    user = User.get(user_id)
    total_treinos = Treino.contar_treinos(user_id)
    
    if user:
        user.total_treinos = total_treinos
        return render_template('profile_personal.html', user_info=user)
    else:
        flash("Usuário não encontrado.")
        return redirect(url_for('index'))