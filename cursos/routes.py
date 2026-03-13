from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Curso, Maestros, db
from sqlalchemy.exc import IntegrityError
import forms

cursos_bp = Blueprint(
    'cursos',
    __name__,
    url_prefix='/cursos'
)

@cursos_bp.route('/', methods=['GET'])
def listar_cursos():
    cursos = Curso.query.all()
    return render_template('cursos_index.html', cursos=cursos)

@cursos_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_curso():
    create_form = forms.CursoForm(request.form)
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()
    ]

    if request.method == 'POST' and create_form.validate():
        maestro_valido = Maestros.query.filter_by(matricula=create_form.maestro_id.data).first()
        if not maestro_valido:
            flash("El maestro seleccionado no existe. Elija un maestro válido.", "error")
            return render_template('agregar_curso.html', form=create_form)

        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )

        try:
            db.session.add(curso)
            db.session.commit()
            flash(f"Curso '{curso.nombre}' agregado correctamente.", "success")
            return redirect(url_for('cursos.listar_cursos'))
        except IntegrityError:
            db.session.rollback()
            flash("Error: no se pudo guardar el curso debido a datos inválidos.", "error")
            return render_template('agregar_curso.html', form=create_form)

    return render_template('agregar_curso.html', form=create_form)

@cursos_bp.route('/detalles/<int:id>', methods=['GET'])
def detalles_curso(id):
    curso = Curso.query.get_or_404(id)
    maestro = Maestros.query.filter_by(matricula=curso.maestro_id).first()
    return render_template('detalles_curso.html', curso=curso, maestro=maestro)

@cursos_bp.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar_curso(id):
    curso = Curso.query.get_or_404(id)
    create_form = forms.CursoForm(request.form, obj=curso)
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()
    ]

    if request.method == 'POST' and create_form.validate():
        maestro_valido = Maestros.query.filter_by(matricula=create_form.maestro_id.data).first()
        if not maestro_valido:
            flash("El maestro seleccionado no existe. Elija un maestro válido.", "error")
            return render_template('modificar_curso.html', form=create_form)

        with db.session.no_autoflush:
            curso.nombre = create_form.nombre.data
            curso.descripcion = create_form.descripcion.data
            curso.maestro_id = create_form.maestro_id.data

            try:
                db.session.commit()
                flash(f"Curso '{curso.nombre}' modificado correctamente.", "success")
                return redirect(url_for('cursos.listar_cursos'))
            except IntegrityError:
                db.session.rollback()
                flash("Error: no se pudo modificar el curso debido a datos inválidos.", "error")
                return render_template('modificar_curso.html', form=create_form)

    return render_template('modificar_curso.html', form=create_form)

@cursos_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    maestro = Maestros.query.filter_by(matricula=curso.maestro_id).first()
    create_form = forms.CursoForm(request.form)

    if request.method == 'POST':
        try:
            for inscripcion in curso.inscripciones:
                db.session.delete(inscripcion)

            db.session.delete(curso)
            db.session.commit()
            flash(f"Curso '{curso.nombre}' y sus inscripciones eliminados correctamente.", "success")
            return redirect(url_for('cursos.listar_cursos'))
        except IntegrityError:
            db.session.rollback()
            flash("Error: no se pudo eliminar el curso debido a restricciones en la base de datos.", "error")
            return render_template('eliminar_curso.html', curso=curso, maestro=maestro, form=create_form)

    return render_template('eliminar_curso.html', curso=curso, maestro=maestro, form=create_form)