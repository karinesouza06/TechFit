from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.User import User
from models import User

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/pagamento', methods=['POST', 'GET'])
@login_required
def pagamento():
    return render_template('pagamento.html')


