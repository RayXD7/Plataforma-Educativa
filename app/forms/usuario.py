from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional

from app.models.auxiliar import RolEnum

# Suponiendo que RolEnum tiene los valores: ADMINISTRADOR, PROFESOR, ESTUDIANTE, JEFE_DEPARTAMENTO
# Si RolEnum es un Enum de Python, puedes hacer algo así:
def obtener_opciones_roles():
    return [(rol.name.lower(), rol.value.capitalize()) for rol in RolEnum]

class CrearUsuarioForm(FlaskForm):
    nombre_completo = StringField('Nombre completo', validators=[
        InputRequired(), Length(min=3, max=100)
    ])
    correo = StringField('Correo electrónico', validators=[
        InputRequired(), Email(), Length(max=100)
    ])
    usuario = StringField('Usuario', validators=[
        InputRequired(), Length(min=4, max=80)
    ])
    clave = PasswordField('Contraseña', validators=[
        InputRequired(), Length(min=6, max=128)
    ])
    rol = SelectField('Rol', choices=obtener_opciones_roles(), validators=[InputRequired()])
    # Agregar un campo para facultad si lo necesitas, por ejemplo:
    # facultad_id = SelectField('Facultad', coerce=int, choices=[])  # Llénalo dinámicamente en la vista

    submit = SubmitField('Crear usuario')

class EditarUsuarioForm(FlaskForm):
    nombre_completo = StringField('Nombre completo', validators=[
        InputRequired(), Length(min=3, max=100)
    ])
    correo = StringField('Correo electrónico', validators=[
        InputRequired(), Email(), Length(max=100)
    ])
    usuario = StringField('Usuario', validators=[
        InputRequired(), Length(min=4, max=80)
    ])
    clave = PasswordField('Contraseña', validators=[
        Optional(), Length(min=6, max=128)
    ])
    rol = SelectField('Rol', choices=obtener_opciones_roles(), validators=[InputRequired()])

    submit = SubmitField('Guardar cambios')

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[InputRequired(), Length(min=4, max=80)])
    clave = PasswordField('Contraseña', validators=[InputRequired(), Length(min=6, max=120)])
    submit = SubmitField('Iniciar sesión')

class ResetPasswordForm(FlaskForm):
    nueva_clave = PasswordField('Nueva contraseña', validators=[
        InputRequired(), Length(min=6, max=128)
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        InputRequired(), EqualTo('nueva_clave', message='Las contraseñas deben coincidir.')
    ])
    require_change = BooleanField('Requerir cambio de contraseña')
    submit = SubmitField('Restablecer')
