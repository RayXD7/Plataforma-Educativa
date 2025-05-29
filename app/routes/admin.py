from flask import Blueprint, flash, redirect, render_template, url_for, request, jsonify, current_app
from flask_login import login_required
from app.models.usuario import Usuario
from app.extensions import db
from app.forms.usuario import CrearUsuarioForm, ResetPasswordForm, EditarUsuarioForm
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dash.html')

@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = CrearUsuarioForm()
    try:
        if form.validate_on_submit():
            existing_user = Usuario.query.filter(
                (Usuario.usuario == form.usuario.data) | (Usuario.correo == form.correo.data)
            ).first()
            if existing_user:
                flash("El nombre de usuario o correo ya está registrado. Por favor, elija otro.", 'warning')
                return redirect(url_for('admin.create_user'))

            new_user = Usuario(
                nombre_completo=form.nombre_completo.data,
                correo=form.correo.data,
                usuario=form.usuario.data,
                clave=generate_password_hash(form.clave.data),
                rol=form.rol.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Usuario registrado con éxito.", 'success')
            return redirect(url_for('admin.list_users'))

        # Mostrar errores de validación WTForms
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en {field}: {error}", 'danger')

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error al crear el usuario: {e}", 'danger')
    except Exception as e:
        # Muestra traceback si estamos en desarrollo
        msg = str(e) if current_app.debug else "Ocurrió un error inesperado."
        flash(f"Excepción: {msg}", 'danger')
    return render_template('users/create.html', form=form)


@admin_bp.route('/list_users')
@login_required
def list_users():
    try:
        users = Usuario.query.all()
        return render_template('users/list.html', users=users)
    except SQLAlchemyError as e:
        flash(f"Error al listar los usuarios: {e}", 'danger')
        return redirect(url_for('admin.create_user'))
    except Exception as e:
        msg = str(e) if current_app.debug else "Ocurrió un error inesperado al listar."
        flash(f"Excepción: {msg}", 'danger')
        return redirect(url_for('admin.create_user'))


@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = EditarUsuarioForm(obj=user)
    try:
        if request.method == 'POST':
            if form.validate_on_submit():
                existing_user = Usuario.query.filter(
                    ((Usuario.usuario == form.usuario.data) | (Usuario.correo == form.correo.data)) &
                    (Usuario.id != user_id)
                ).first()
                if existing_user:
                    return jsonify(success=False, message="Usuario o correo en uso."), 409

                user.nombre_completo = form.nombre_completo.data
                user.correo = form.correo.data
                user.usuario = form.usuario.data
                user.rol = form.rol.data
                if form.clave.data:
                    user.clave = generate_password_hash(form.clave.data)

                db.session.commit()
                return jsonify(success=True, message="Usuario actualizado.", redirect_url=url_for('admin.list_users'))

            return jsonify(success=False, message="Errores de validación", errors=form.errors), 400

        # GET
        return render_template('users/edit.html', form=form, user=user)

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(success=False, message=f"DB Error: {e}"), 500
    except Exception as e:
        msg = str(e) if current_app.debug else "Error inesperado."
        return jsonify(success=False, message=f"Excepción: {msg}"), 500


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
        flash(f"Error al eliminar el usuario: {e}", 'danger')
    except Exception as e:
        msg = str(e) if current_app.debug else "Error inesperado al eliminar."
        flash(f"Excepción: {msg}", 'danger')
    return redirect(url_for('admin.list_users'))


@admin_bp.route('/detail_user/<int:user_id>')
@login_required
def detail_user(user_id):
    try:
        user = Usuario.query.get_or_404(user_id)
        return render_template('users/details.html', user=user)
    except Exception as e:
        msg = str(e) if current_app.debug else "Error inesperado al obtener detalles."
        flash(f"Excepción: {msg}", 'danger')
        return redirect(url_for('admin.list_users'))


@admin_bp.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def reset_password(user_id):
    user = Usuario.query.get_or_404(user_id)
    form = ResetPasswordForm()
    try:
        if request.method == 'POST':
            if form.validate_on_submit():
                user.clave = generate_password_hash(form.nueva_clave.data)
                db.session.commit()
                return jsonify(success=True, message="Contraseña restablecida.", redirect_url=url_for('admin.list_users'))
            return jsonify(success=False, message="Errores de validación", errors=form.errors), 400

        return render_template('users/reset.html', form=form, user=user)

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(success=False, message=f"DB Error: {e}"), 500
    except Exception as e:
        msg = str(e) if current_app.debug else "Error inesperado."
        return jsonify(success=False, message=f"Excepción: {msg}"), 500
