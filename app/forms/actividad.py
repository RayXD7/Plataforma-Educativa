from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime

class ActividadForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=2000)])
    fecha = DateTimeLocalField('Fecha y Hora', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_fecha(self, field):
        """
        Validación personalizada para asegurar que la fecha no sea menor a la actual.
        """
        if field.data < datetime.now():
            raise ValidationError('La fecha y hora debe ser igual o posterior a la fecha actual.')

class EnviarActividadForm(FlaskForm):
    submit = SubmitField('Enviar')
    