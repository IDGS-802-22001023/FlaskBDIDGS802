from flask import Flask, render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms

# Migracion de BD
from flask_migrate import Migrate

# Registro de modulos
from maestros.routes import maestros_bp # Que se no se repitan carpetas

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros_bp) # Aqui se registra maestros, para no tener que repetir codigo
csrf = CSRFProtect()
db.init_app(app)
migrate = Migrate(app,db)

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html")

@app.route("/", methods=["GET","POST"])
@app.route("/index")
def index():
    create_form=forms.UserForm(request.form)
    #tem= Alumnos.query('select * from alumnos')
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form,alumno=alumno)

@app.route("/Alumnos",methods=["GET","POST"])
def alumnos():
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        alum = Alumnos(
            nombre = create_form.nombre.data,
            apellidos = create_form.apellidos.data,
            telefono = create_form.telefono.data,
            email = create_form.email.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos.html",form=create_form)

@app.route("/detalles",methods=["GET","POST"])
def detalles():
    if request.method=='GET':
        id = request.args.get('id')
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nombre = alum.nombre
        apellidos = alum.apellidos
        telefono = alum.telefono
        email = alum.email
    return render_template("detalles.html",alum=alum,nombre=nombre, apellidos = apellidos,telefono=telefono, email=email)

@app.route("/modificar",methods=["GET","POST"])
def modificar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id = request.args.get('id')
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum.nombre
        create_form.apellidos.data=alum.apellidos
        create_form.telefono.data=alum.telefono
        create_form.email.data=alum.email
    if request.method=='POST':
        id = create_form.id.data
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.id = id
        alum.nombre = str.rstrip(create_form.nombre.data)
        alum.apellidos = create_form.apellidos.data
        alum.telefono = create_form.telefono.data
        alum.email = create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("modificar.html",form=create_form,nombre=create_form.nombre.data, apellidos = create_form.apellidos.data, email=create_form.email.data)

@app.route("/eliminar",methods=["GET","POST"])
def eliminar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id = request.args.get('id')
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum.nombre
        create_form.apellidos.data=alum.apellidos
        create_form.telefono.data=alum.telefono
        create_form.email.data=alum.email
    if request.method=='POST':
        id = create_form.id.data
        alum= db.session.query(Alumnos).get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html",form=create_form)

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# flask db migrate -m "Primera migracion"
# flask db upgrade

# Modificacion de lamodel

# flask db migrate -m "Alumnos con cambios en los campos"
# flask db upgrade