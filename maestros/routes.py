from flask import Blueprint, render_template, request, redirect, url_for
from models import Maestros, db
import forms

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/maestros'
)

# ===============================
# LISTAR MAESTROS
# ===============================
@maestros_bp.route('/', methods=['GET'])
def listar_maestros():
    maestros = Maestros.query.all()
    return render_template(
        'maestros_index.html',
        maestros=maestros
    )

# ===============================
# AGREGAR MAESTRO
# ===============================
@maestros_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_maestro():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'POST':
        maestro = Maestros(
            matricula=create_form.matricula.data,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        return redirect(url_for('maestros.listar_maestros'))

    return render_template(
        'agregar_maestro.html',
        form=create_form
    )

# ===============================
# DETALLES MAESTRO
# ===============================
@maestros_bp.route('/detalles', methods=['GET'])
def detalles_maestro():
    id = request.args.get('id')
    maestro = Maestros.query.get(id)

    return render_template(
        'detalles_maestro.html',
        maestro=maestro
    )

# ===============================
# MODIFICAR MAESTRO
# ===============================
@maestros_bp.route('/modificar', methods=['GET', 'POST'])
def modificar_maestro():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        maestro = Maestros.query.get(id)

        create_form.id.data = maestro.id
        create_form.matricula.data = maestro.matricula
        create_form.nombre.data = maestro.nombre
        create_form.apellidos.data = maestro.apellidos
        create_form.especialidad.data = maestro.especialidad
        create_form.email.data = maestro.email

    if request.method == 'POST':
        maestro = Maestros.query.get(create_form.id.data)

        maestro.matricula = create_form.matricula.data
        maestro.nombre = create_form.nombre.data
        maestro.apellidos = create_form.apellidos.data
        maestro.especialidad = create_form.especialidad.data
        maestro.email = create_form.email.data

        db.session.commit()
        return redirect(url_for('maestros.listar_maestros'))

    return render_template(
        'modificar_Maestro.html',
        form=create_form
    )

# ===============================
# ELIMINAR MAESTRO
# ===============================
@maestros_bp.route('/eliminar', methods=['GET', 'POST'])
def eliminar_maestro():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        maestro = Maestros.query.get(id)

        create_form.id.data = maestro.id
        create_form.nombre.data = maestro.nombre
        create_form.apellidos.data = maestro.apellidos
        create_form.email.data = maestro.email

    if request.method == 'POST':
        maestro = Maestros.query.get(create_form.id.data)
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for('maestros.listar_maestros'))

    return render_template(
        'eliminar_Maestro.html',
        form=create_form
    )