from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_user, login_required, logout_user

from werkzeug.security import check_password_hash

from app.models.usuario import Usuario
from app.forms.usuario import LoginForm


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard',))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Usuario.query.filter_by(usuario=form.usuario.data).first()
            if user and check_password_hash(user.clave, form.clave.data):
                login_user(user)
                flash('Bienvenido, ' + user.usuario)
                return redirect(url_for('admin.dashboard'))  # Dashboard único
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
