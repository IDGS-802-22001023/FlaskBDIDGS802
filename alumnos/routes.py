from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Alumnos, db
import forms

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/alumnos'
)

@alumnos_bp.route('/', methods=['GET'])
def listar_alumnos():
    alumnos = Alumnos.query.all()
    return render_template(
        'alumnos_index.html',
        alumnos=alumnos
    )

@alumnos_bp.route('/agregar', methods=['GET','POST'])
def agregar_alumno():
    create_form = forms.UserForm(request.form)  
    if request.method == 'POST':
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            telefono=create_form.telefono.data,
            email=create_form.email.data
        )
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for('alumnos.listar_alumnos'))
    return render_template(
        'alumnos.html',
        form=create_form
    )

@alumnos_bp.route('/detalles', methods=['GET'])
def detalles_alumno():
    id = request.args.get('id')
    alumno = Alumnos.query.get(id)
    return render_template(
        'detalles.html',
        alumno=alumno
    )

@alumnos_bp.route('/modificar', methods=['GET','POST'])
def modificar_alumno():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumno = Alumnos.query.get(id)
        create_form.id.data = alumno.id
        create_form.nombre.data = alumno.nombre
        create_form.apellidos.data = alumno.apellidos
        create_form.telefono.data = alumno.telefono
        create_form.email.data = alumno.email
    if request.method == 'POST':
        alumno = Alumnos.query.get(create_form.id.data)
        alumno.nombre = create_form.nombre.data
        alumno.apellidos = create_form.apellidos.data
        alumno.telefono = create_form.telefono.data
        alumno.email = create_form.email.data
        db.session.commit()
        return redirect(url_for('alumnos.listar_alumnos'))
    return render_template(
        'modificar.html',
        form=create_form
    )

@alumnos_bp.route('/eliminar', methods=['GET', 'POST'])
def eliminar_alumno():
    create_form = forms.UserForm(request.form)
    id_alumno = request.args.get('id')
    alumno = Alumnos.query.get(id_alumno)
    if not alumno:
        flash("Alumno no encontrado.", "error")
        return redirect(url_for('alumnos.listar_alumnos'))

    create_form.id.data = alumno.id
    create_form.nombre.data = alumno.nombre
    create_form.apellidos.data = alumno.apellidos
    create_form.telefono.data = alumno.telefono
    create_form.email.data = alumno.email

    if request.method == 'POST' and create_form.validate():
        if alumno.cursos:
            flash("No se puede eliminar este alumno. Tiene inscripciones.", "error")
            return redirect(url_for('alumnos.listar_alumnos'))
        db.session.delete(alumno)
        db.session.commit()
        flash("Alumno eliminado correctamente.", "success")
        return redirect(url_for('alumnos.listar_alumnos'))

    return render_template('eliminar.html', form=create_form)