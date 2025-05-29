from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models.encuesta import Encuesta
from app.models.actividad import Actividad
from app.extensions import db

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dash.html')

@teacher_bp.route('/view_surveys', methods=['GET'])
@login_required
def view_surveys():
    """
    Muestra las encuestas asignadas al profesor autenticado.
    """
    try:
        surveys = Encuesta.query.filter_by(profesor_id=current_user.id).all()
        return render_template('teacher/view_surveys.html', surveys=surveys)
    except SQLAlchemyError as e:
        current_app.logger.error(f"DB Error view_surveys: {e}")
        msg = str(e) if current_app.debug else 'Error al cargar las encuestas.'
        flash(msg, 'danger')
        return redirect(url_for('teacher.dashboard'))
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al mostrar encuestas.'
        flash(msg, 'danger')
        return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/list_activities', methods=['GET'])
@login_required
def list_activities():
    """
    Lista las actividades creadas o asignadas al profesor.
    """
    try:
        page = request.args.get('page', 1, type=int)
        pagination = Actividad.query.filter_by(profesor_id=current_user.id) \
            .order_by(Actividad.fecha.desc()) \
            .paginate(page=page, per_page=10, error_out=False)
        return render_template('teacher/list_activities.html', activities=pagination)
    except SQLAlchemyError as e:
        current_app.logger.error(f"DB Error list_activities(teacher): {e}")
        msg = str(e) if current_app.debug else 'Error al listar actividades.'
        flash(msg, 'danger')
        return redirect(url_for('teacher.dashboard'))
    except Exception as e:
        msg = str(e) if current_app.debug else 'Error inesperado al listar actividades.'
        flash(msg, 'danger')
        return redirect(url_for('teacher.dashboard'))
