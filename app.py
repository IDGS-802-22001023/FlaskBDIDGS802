from flask import Flask, render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect()

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
            apaterno = create_form.aPaterno.data,
            email = create_form.email.data
        )
        db.session.add(alum)
        db.session.commit()
    return render_template("alumnos.html",form=create_form)

@app.route("/detalles",methods=["GET","POST"])
def detalles():
    if request.method=='GET':
        id = request.args.get('id')
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        id = request.args.get('id')
        nombre = alum.nombre
        apaterno = alum.apaterno
        email = alum.email
    return render_template("detalles.html",nombre=nombre, apaterno = apaterno, email=email)

@app.route("/modificar",methods=["GET","POST"])
def modificar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id = request.args.get('id')
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum.nombre
        create_form.aPaterno.data=alum.apaterno
        create_form.email.data=alum.email
    if request.method=='POST':
        id = create_form.id.data
        alum= db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.id = id
        alum.nombre = str.rstrip(create_form.nombre.data)
        alum.apaterno = create_form.aPaterno.data
        alum.email = create_form.email.data
        db.session.add(alum)
        db.session.commit()
    return render_template("modificar.html",form=create_form,nombre=create_form.nombre.data, apaterno = create_form.aPaterno.data, email=create_form.email.data)

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)