import csv
import io
from flask import Blueprint, Response, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.actividad import Actividad
from app.models.auxiliar import TipoActividadEnum
from flask_wtf import FlaskForm
from wtforms import SubmitField

# Formulario minimalista para CSRF en toggles
class ToggleTipoForm(FlaskForm):
    submit = SubmitField('Toggle')

jefe_bp = Blueprint('jefe_departamento', __name__, url_prefix='/jefe')

# Decorator de ejemplo para roles (ajusta según tu implementación)
def roles_required(role):
    def wrapper(fn):
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol.value != role:
                abort(403)
            return fn(*args, **kwargs)
        decorated_view.__name__ = fn.__name__
        return login_required(decorated_view)
    return wrapper

@jefe_bp.route('/activities', methods=['GET'])
@login_required
def list_activities():
    """
    Lista actividades oficiales enviadas para revisión, con paginación.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 5
    # Solo actividades enviadas y oficiales
    query = Actividad.query.filter_by(enviada=True, tipo=TipoActividadEnum.NO_OFICIAL)
    pagination = query.order_by(Actividad.fecha.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template(
        'jefe_departamento/list_activities.html',
        activities=pagination,
        form_csrf=ToggleTipoForm()
    )

@jefe_bp.route('/activities/toggle_tipo/<int:actividad_id>', methods=['POST'])
@roles_required('jefe_departamento')
def toggle_tipo(actividad_id):
    """
    Cambia el tipo de actividad entre OFICIAL y NO_OFICIAL.
    """
    actividad = Actividad.query.get_or_404(actividad_id)
    form = ToggleTipoForm()
    if not form.validate_on_submit():
        flash('Token CSRF inválido.', 'danger')
        return redirect(url_for('jefe_departamento.list_activities'))

    if not actividad.enviada:
        flash('Sólo se pueden procesar actividades enviadas.', 'warning')
        return redirect(url_for('jefe_departamento.list_activities'))

    # Toggle oficial/no oficial
    if actividad.tipo == TipoActividadEnum.OFICIAL:
        actividad.tipo = TipoActividadEnum.NO_OFICIAL
        msg = 'Actividad cambiada a No Oficial.'
    else:
        actividad.tipo = TipoActividadEnum.OFICIAL
        msg = 'Actividad marcada como Oficial.'

    try:
        db.session.commit()
        flash(msg, 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('Error al actualizar el tipo de actividad.', 'danger')

    return redirect(url_for('jefe_departamento.list_activities', page=request.args.get('page', 1)))

@jefe_bp.route('/activities/export', methods=['GET'])
@roles_required('jefe_departamento')
def export_activities():
    """
    Exporta las actividades oficiales enviadas a un CSV descargable.
    """
    activities = Actividad.query.filter_by(enviada=True, tipo=TipoActividadEnum.OFICIAL) \
        .order_by(Actividad.fecha.desc()).all()

    proxy = io.StringIO()
    writer = csv.writer(proxy)
    writer.writerow(['ID', 'Título', 'Tipo', 'Fecha', 'Creador'])
    for act in activities:
        writer.writerow([
            act.id,
            act.titulo,
            act.tipo.value,
            act.fecha.strftime('%Y-%m-%d %H:%M'),
            act.creador.usuario
        ])

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    mem.seek(0)
    proxy.close()

    return Response(
        mem,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment;filename=actividades_oficiales.csv'
        }
    )
