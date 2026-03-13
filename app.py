from flask import Flask, render_template, request
from flask import flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from flask_migrate import Migrate

from maestros.routes import maestros_bp
from alumnos.routes import alumnos_bp
from cursos.routes import cursos_bp
from inscripciones.routes import inscripciones_bp

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)

csrf = CSRFProtect()

db.init_app(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    alumno = Alumnos.query.all()

    return render_template(
        "index.html",
        form=create_form,
        alumno=alumno
    )


if __name__ == '__main__':
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True)