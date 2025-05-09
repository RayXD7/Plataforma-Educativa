from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required
from app.models.usuario import Usuario
from app.extensions import db
from app.forms.usuario import CrearUsuarioForm, ResetPasswordForm  # Asegúrate de importar tu form
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dash.html')

# Crear Usuario
@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = CrearUsuarioForm()
    if form.validate_on_submit():
        try:
            # Verificar si el usuario o correo ya existen
            existing_user = Usuario.query.filter(
                (Usuario.usuario == form.usuario.data) | (Usuario.correo == form.correo.data)
            ).first()
            if existing_user:
                flash("El nombre de usuario o correo ya está registrado. Por favor, elija otro.", 'danger')
                return redirect(url_for('admin.create_user'))

            # Crear el nuevo usuario
            password_hash = generate_password_hash(form.clave.data)
            new_user = Usuario(
                nombre_completo=form.nombre_completo.data,
                correo=form.correo.data,
                usuario=form.usuario.data,
                clave=password_hash,
                rol=form.rol.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Usuario registrado con éxito.", 'success')
            return redirect(url_for('admin.list_users'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error al crear el usuario: {str(e)}", 'danger')

    # Mostrar errores si existen
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en el campo {field}: {error}", 'danger')

    return render_template('users/create.html', form=form)

# Listar Usuarios
@admin_bp.route('/list_users')
@login_required
def list_users():
    try:
        users = Usuario.query.all()
        return render_template('users/list.html', users=users)
    except SQLAlchemyError as e:
        flash(f"Error al listar los usuarios: {str(e)}", 'danger')
        return redirect(url_for('admin.create_user'))

# Editar Usuario
@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = CrearUsuarioForm(obj=user)
    if form.validate_on_submit():
        try:
            # Verificar si el nombre de usuario o correo ya existen (y no es el mismo usuario)
            existing_user = Usuario.query.filter(
                ((Usuario.usuario == form.usuario.data) | (Usuario.correo == form.correo.data)) &
                (Usuario.id != user_id)
            ).first()
            if existing_user:
                flash("El nombre de usuario o correo ya está en uso. Por favor, elija otro.", 'danger')
                return redirect(url_for('admin.edit_user', user_id=user.id))

            # Actualizar los datos del usuario
            user.nombre_completo = form.nombre_completo.data
            user.correo = form.correo.data
            user.usuario = form.usuario.data
            user.rol = form.rol.data
            if form.clave.data:
                user.clave = generate_password_hash(form.clave.data)
            db.session.commit()
            flash("Usuario actualizado con éxito.", 'success')
            return redirect(url_for('admin.list_users'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error al actualizar el usuario: {str(e)}", 'danger')

    # Prellenar los datos del formulario con la información del usuario
    if request.method == 'GET':
        form.nombre_completo.data = user.nombre_completo
        form.correo.data = user.correo
        form.usuario.data = user.usuario
        form.rol.data = user.rol
        # Nota: No prellenes la contraseña por seguridad

    return render_template('users/edit.html', form=form, user=user)

# Eliminar Usuario
@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    try:
        user = Usuario.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("Usuario eliminado con éxito.", 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al eliminar el usuario: {str(e)}", 'danger')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/detail_user/<int:user_id>')
@login_required
def detail_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    return render_template('users/details.html', user=user)


@admin_bp.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def reset_password(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            user.clave = generate_password_hash(form.nueva_clave.data)
            db.session.commit()
            flash("Contraseña restablecida con éxito.", "success")
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al restablecer la contraseña: {str(e)}", "danger")
    return render_template('users/reset.html', form=form, user=user)


