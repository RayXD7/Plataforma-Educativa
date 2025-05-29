from flask import Blueprint, render_template, request
from app.models.actividad import Actividad
from app.models.auxiliar import TipoActividadEnum

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    # Consultar solo actividades oficiales ordenadas por fecha descendente
    pagination = Actividad.query.filter_by(tipo=TipoActividadEnum.OFICIAL).order_by(Actividad.fecha.desc()).paginate(page=page, per_page=per_page)

    return render_template('index.html', activities=pagination)
