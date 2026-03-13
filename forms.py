from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    id = HiddenField()
    nombre = StringField(
        'Nombre Alumno',
        validators=[DataRequired(message="El campo es requerido"), Length(min=3, max=50)]
    )
    apellidos = StringField(
        'Apellidos',
        validators=[DataRequired(message="El campo es requerido")]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(message="Ingrese un correo válido")]
    )
    telefono = StringField(
        'Teléfono',
        validators=[DataRequired(), Length(min=8, max=20)]
    )
    submit = SubmitField('Guardar')


class MaestroForm(FlaskForm):
    id = HiddenField()
    matricula = StringField(
        'Matrícula',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    nombre = StringField(
        'Nombre Maestro',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    apellidos = StringField(
        'Apellidos',
        validators=[DataRequired()]
    )
    especialidad = StringField(
        'Especialidad',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Guardar')


class CursoForm(FlaskForm):
    id = HiddenField()
    nombre = StringField(
        'Nombre del Curso',
        validators=[DataRequired(), Length(min=3, max=150)]
    )
    descripcion = StringField(
        'Descripción del Curso',
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    maestro_id = StringField(
        'Matrícula del Maestro',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    submit = SubmitField('Guardar')


class InscripcionForm(FlaskForm):
    alumno_id = SelectField(
        'Alumno',
        coerce=int,
        validators=[DataRequired()]
    )
    curso_id = SelectField(
        'Curso',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Guardar')