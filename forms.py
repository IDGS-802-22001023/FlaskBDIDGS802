from wtforms import Form, RadioField
from wtforms import StringField, IntegerField, PasswordField
from wtforms import EmailField
from wtforms import validators


class UserForm(Form): #HEREDA DE LA CLASE FORM
    id = IntegerField('ID',[
        validators.DataRequired(message="El campo es requerido")
        ])
    nombre = StringField('Nombre Alumno', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message="Ingrese un nombre valido")
    ])
    aPaterno = StringField('Apaterno',[
        validators.DataRequired(message="El campo es requerido"),
    ])
    email = EmailField('Email', [
        validators.Email(message="Ingrese un correo valido"),
    ])