from flask import render_template, redirect, url_for, flash, Blueprint, current_app, request
from flask_login import current_user, login_user, login_required, logout_user

from werkzeug.security import check_password_hash

from app.models.usuario import Usuario
from app.forms.usuario import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está autenticado, redirige al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Usuario.query.filter_by(usuario=form.usuario.data).first()
            if user and check_password_hash(user.clave, form.clave.data):
                login_user(user)
                flash(f'Bienvenido, {user.usuario}', 'success')
                # Redirige al siguiente si existe o al dashboard
                next_page = request.args.get('next') or url_for('admin.dashboard')
                return redirect(next_page)
            else:
                flash('Usuario o contraseña incorrectos.', 'danger')
        except Exception as e:
            # Muestra el error completo en modo debug, o un mensaje genérico en producción
            msg = str(e) if current_app.debug else 'Error interno al procesar el inicio de sesión.'
            flash(f'Error al iniciar sesión: {msg}', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
