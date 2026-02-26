from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):

    id = HiddenField()

    nombre = StringField(
        'Nombre Alumno',
        validators=[
            DataRequired(message="El campo es requerido"),
            Length(min=3, max=50, message="Ingrese un nombre válido")
        ]
    )

    apellidos = StringField(
        'Apellidos',
        validators=[
            DataRequired(message="El campo es requerido")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="El campo es requerido"),
            Email(message="Ingrese un correo válido")
        ]
    )

    telefono = StringField(
        'Teléfono',
        validators=[
            DataRequired(message="El campo es requerido"),
            Length(min=8, max=20, message="Ingrese un teléfono válido")
        ]
    )

    submit = SubmitField('Guardar')