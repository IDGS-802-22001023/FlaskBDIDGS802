from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Inscripcion, Alumnos, Curso, db
from forms import InscripcionForm
import forms

inscripciones_bp = Blueprint(
    'inscripciones',
    __name__,
    url_prefix='/inscripciones'
)

@inscripciones_bp.route('/', methods=['GET'])
def listar_inscripciones():
    inscripciones = Inscripcion.query.all()
    return render_template(
        'inscripciones_index.html',
        inscripciones=inscripciones
    )

@inscripciones_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_inscripcion():
    create_form = InscripcionForm(request.form)
    create_form.alumno_id.choices = [
        (a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()
    ]
    create_form.curso_id.choices = [
        (c.id, c.nombre) for c in Curso.query.all()
    ]

    if request.method == 'POST' and create_form.validate():
        existe = Inscripcion.query.filter_by(
            alumno_id=create_form.alumno_id.data,
            curso_id=create_form.curso_id.data
        ).first()
        if existe:
            flash("El alumno ya está inscrito en este curso.", "error")
            return redirect(url_for('inscripciones.agregar_inscripcion'))

        inscripcion = Inscripcion(
            alumno_id=create_form.alumno_id.data,
            curso_id=create_form.curso_id.data
        )
        db.session.add(inscripcion)
        db.session.commit()
        flash("Inscripción guardada exitosamente.", "success")
        return redirect(url_for('inscripciones.listar_inscripciones'))

    return render_template('agregar_inscripcion.html', form=create_form)

@inscripciones_bp.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    create_form = InscripcionForm(obj=inscripcion)
    create_form.alumno_id.choices = [
        (a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()
    ]
    create_form.curso_id.choices = [
        (c.id, c.nombre) for c in Curso.query.all()
    ]

    if request.method == 'POST' and create_form.validate():
        existe = Inscripcion.query.filter_by(
            alumno_id=create_form.alumno_id.data,
            curso_id=create_form.curso_id.data
        ).first()
        if existe and existe.id != inscripcion.id:
            flash("El alumno ya está inscrito en este curso.", "error")
            return redirect(url_for('inscripciones.modificar_inscripcion', id=id))

        inscripcion.alumno_id = create_form.alumno_id.data
        inscripcion.curso_id = create_form.curso_id.data
        db.session.commit()
        flash("Inscripción modificada exitosamente.", "success")
        return redirect(url_for('inscripciones.listar_inscripciones'))

    return render_template('modificar_inscripcion.html', form=create_form)

@inscripciones_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_inscripcion(id):
    create_form = forms.InscripcionForm(request.form)
    inscripcion = Inscripcion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(inscripcion)
        db.session.commit()
        flash("Inscripción eliminada exitosamente.", "success")
        return redirect(url_for('inscripciones.listar_inscripciones'))
    return render_template('eliminar_inscripcion.html', inscripcion=inscripcion, form=create_form)

@inscripciones_bp.route('/detalles/<int:id>', methods=['GET'])
def detalles_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    alumno = Alumnos.query.get(inscripcion.alumno_id)
    curso = Curso.query.get(inscripcion.curso_id)
    return render_template(
        'detalles_inscripcion.html',
        inscripcion=inscripcion,
        alumno=alumno,
        curso=curso
    )