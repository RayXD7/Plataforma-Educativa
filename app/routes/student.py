from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.actividad import Actividad
from app.models.auxiliar import TipoActividadEnum
from app.forms.actividad import ActividadForm, EnviarActividadForm

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/activities', methods=['GET'])
@login_required
def list_activities():
    """
    Lista todas las actividades del usuario autenticado, paginadas.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        pagination = Actividad.query.filter_by(creador_id=current_user.id) \
            .order_by(Actividad.fecha.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)
        return render_template(
            'student/activities.html',
            activities=pagination,
            form_envio=EnviarActividadForm(),
        )
    except SQLAlchemyError as e:
        current_app.logger.error(f"DB Error list_activities: {e}")
        flash('Error al cargar las actividades.', 'danger')
        return render_template('student/activities.html', activities=None)
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al listar actividades.'
        flash(msg, 'danger')
        return render_template('student/activities.html', activities=None)

@student_bp.route('/activities/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    """
    Crea una nueva actividad.
    """
    form = ActividadForm()
    try:
        if form.validate_on_submit():
            actividad = Actividad(
                titulo=form.titulo.data,
                descripcion=form.descripcion.data,
                fecha=form.fecha.data,
                creador_id=current_user.id
            )
            db.session.add(actividad)
            db.session.commit()
            flash('Actividad creada con éxito.', 'success')
            return redirect(url_for('student.list_activities'))
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"DB Error create_activity: {e}")
        flash(f'Error al crear la actividad: {e}', 'danger')
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al crear actividad.'
        flash(msg, 'danger')

    # Si GET o hay fallo
    return render_template(
        'student/create_activities.html',
        form=form,
        title='Crear Actividad'
    )

@student_bp.route('/activities/edit/<int:actividad_id>', methods=['GET', 'POST'])
@login_required
def edit_activity(actividad_id):
    """
    Edita una actividad existente si el usuario es el creador.
    """
    try:
        actividad = Actividad.query.get_or_404(actividad_id)
        if actividad.creador_id != current_user.id:
            abort(403)

        form = ActividadForm(obj=actividad)
        if form.validate_on_submit():
            actividad.titulo = form.titulo.data
            actividad.descripcion = form.descripcion.data
            actividad.fecha = form.fecha.data
            db.session.commit()
            flash('Actividad actualizada con éxito.', 'success')
            return redirect(url_for('student.list_activities'))
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"DB Error edit_activity: {e}")
        flash(f'Error al actualizar la actividad: {e}', 'danger')
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al editar actividad.'
        flash(msg, 'danger')
        return redirect(url_for('student.list_activities'))

    return render_template(
        'student/create_activities.html',
        form=form,
        title='Editar Actividad'
    )

@student_bp.route('/activities/detail/<int:actividad_id>', methods=['GET'])
@login_required
def detail_activity(actividad_id):
    """
    Muestra los detalles de una actividad.
    """
    try:
        actividad = Actividad.query.get_or_404(actividad_id)
        if actividad.creador_id != current_user.id:
            abort(403)
        return render_template(
            'student/detail_activity.html',
            actividad=actividad
        )
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al mostrar detalles.'
        flash(msg, 'danger')
        return redirect(url_for('student.list_activities'))

@student_bp.route('/activities/delete/<int:actividad_id>', methods=['POST'])
@login_required
def delete_activity(actividad_id):
    """
    Elimina una actividad si el usuario es el creador.
    """
    try:
        actividad = Actividad.query.get_or_404(actividad_id)
        if actividad.creador_id != current_user.id:
            abort(403)
        db.session.delete(actividad)
        db.session.commit()
        flash('Actividad eliminada con éxito.', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"DB Error delete_activity: {e}")
        flash(f'Error al eliminar la actividad: {e}', 'danger')
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al eliminar.'
        flash(msg, 'danger')
    return redirect(url_for('student.list_activities'))

@student_bp.route('/activities/submit/<int:actividad_id>', methods=['POST'])
@login_required
def submit_activity(actividad_id):
    """
    Marca una actividad como enviada o informa si ya fue enviada.
    """
    try:
        actividad = Actividad.query.get_or_404(actividad_id)
        if actividad.creador_id != current_user.id:
            abort(403)

        form = EnviarActividadForm()
        if not form.validate_on_submit():
            flash('Token CSRF inválido o solicitud incorrecta.', 'danger')
            return redirect(url_for('student.list_activities'))

        if actividad.enviada:
            flash('Esta actividad ya fue enviada previamente.', 'info')
        else:
            actividad.enviada = True
            db.session.commit()
            flash('Actividad enviada con éxito.', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"DB Error submit_activity: {e}")
        flash(f'Error al enviar la actividad: {e}', 'danger')
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al enviar.'
        flash(msg, 'danger')
    return redirect(url_for('student.list_activities'))
