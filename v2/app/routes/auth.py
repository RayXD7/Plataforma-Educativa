from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user

from app.models.usuario import Usuario
from app.forms.usuario import LoginForm


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and user.password == password:  # Usa hash en producción
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('auth/login.html', form=LoginForm())

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
