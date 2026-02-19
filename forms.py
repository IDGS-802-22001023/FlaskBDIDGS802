from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, EmailField
from wtforms import validators


class UserForm(FlaskForm):
    matricula = IntegerField(
        'Matricula',
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.NumberRange(min=100, max=1000, message='Ingrese un valor válido')
        ]
    )

    nombre = StringField(
        "Nombre",
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.Length(min=3, max=10)
        ]
    )

    apaterno = StringField(
        "Apaterno",
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.Length(min=3, max=10)
        ]
    )

    amaterno = StringField(
        "Amaterno",
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.Length(min=3, max=10)
        ]
    )

    correo = EmailField(
        "Correo",
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.Email(message="Email no válido")
        ]
    )


class cineForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.Length(min=3, max=10)
        ]
    )

    numCompradores = IntegerField(
        'Cantidad de compradores',
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.NumberRange(min=1, max=50)
        ]
    )

    numBoletos = IntegerField(
        'Cantidad de boletos',
        validators=[
            validators.DataRequired(message='Campo requerido'),
            validators.NumberRange(min=1, max=100)
        ]
    )

    tarjeta = RadioField(
        "Tarjeta Cinépolis",
        choices=[('no', 'No'), ('si', 'Sí')],
        validators=[validators.DataRequired(message='Seleccione una opción')]
    )
