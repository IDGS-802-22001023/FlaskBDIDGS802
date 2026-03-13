from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Maestros, db
import forms

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/maestros'
)

@maestros_bp.route('/', methods=['GET'])
def listar_maestros():
    maestros = Maestros.query.all()
    return render_template(
        'maestros_index.html',
        maestros=maestros
    )
    
@maestros_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_maestro():
    create_form = forms.MaestroForm(request.form)
    if request.method == 'POST' and create_form.validate():
        existe = Maestros.query.get(create_form.matricula.data)
        if existe:
            flash("Ya existe un maestro con esta matrícula.", "error")
            return redirect(url_for('maestros.agregar_maestro'))

        maestro = Maestros(
            matricula=create_form.matricula.data,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        flash("Maestro agregado correctamente.", "success")
        return redirect(url_for('maestros.listar_maestros'))

    return render_template(
        'agregar_maestro.html',
        form=create_form
    )

@maestros_bp.route('/detalles', methods=['GET'])
def detalles_maestro():
    matricula = request.args.get('matricula')
    maestro = Maestros.query.get(matricula)
    return render_template(
        'detalles_maestro.html',
        maestro=maestro
    )

@maestros_bp.route('/modificar', methods=['GET', 'POST'])
def modificar_maestro():
    create_form = forms.MaestroForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro = Maestros.query.get(matricula)
        create_form.matricula.data = maestro.matricula
        create_form.nombre.data = maestro.nombre
        create_form.apellidos.data = maestro.apellidos
        create_form.especialidad.data = maestro.especialidad
        create_form.email.data = maestro.email

    if request.method == 'POST' and create_form.validate():
        if create_form.matricula.data != request.args.get('matricula'):
            existe = Maestros.query.get(create_form.matricula.data)
            if existe:
                flash("Ya existe un maestro con esta matrícula.", "error")
                return redirect(url_for('maestros.modificar_maestro', matricula=request.args.get('matricula')))

        maestro = Maestros.query.get(request.args.get('matricula'))
        maestro.matricula = create_form.matricula.data
        maestro.nombre = create_form.nombre.data
        maestro.apellidos = create_form.apellidos.data
        maestro.especialidad = create_form.especialidad.data
        maestro.email = create_form.email.data

        db.session.commit()
        flash("Maestro modificado correctamente.", "success")
        return redirect(url_for('maestros.listar_maestros'))

    return render_template(
        'modificar_maestro.html',
        form=create_form
    )

@maestros_bp.route('/eliminar', methods=['GET', 'POST'])
def eliminar_maestro():
    create_form = forms.MaestroForm(request.form)
    matricula = request.args.get('matricula')
    maestro = Maestros.query.get(matricula)

    if maestro.cursos:
        flash("No se puede eliminar este maestro. Tiene cursos asignados.", "error")
        return redirect(url_for('maestros.listar_maestros'))

    if request.method == 'POST':
        db.session.delete(maestro)
        db.session.commit()
        flash("Maestro eliminado correctamente.", "success")
        return redirect(url_for('maestros.listar_maestros'))

    create_form.matricula.data = maestro.matricula
    create_form.nombre.data = maestro.nombre
    create_form.apellidos.data = maestro.apellidos
    create_form.email.data = maestro.email
    create_form.especialidad.data = maestro.especialidad

    return render_template(
        'eliminar_Maestro.html',
        form=create_form
    )