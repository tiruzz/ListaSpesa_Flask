from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from moduls import db, ListaSpesa

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista_spesa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

lista_spese = []


@app.route('/')
def home():
    lista_spesa = ListaSpesa.query.all()

    return render_template('index.html' , lista_spese = lista_spesa) 

@app.route('/add', methods=['POST'])
def add():
    elemento = request.form['elemento']
    if elemento:
        nuovo_elemento = ListaSpesa(elemento=elemento)
        db.session.add(nuovo_elemento) 
        db.session.commit() 
       
    return redirect(url_for('home'))

@app.route('/remove/<int:indice>', methods=['POST'])
def remove(indice):
    elemento = ListaSpesa.query.get_or_404(indice)
    db.session.delete(elemento)
    db.session.commit() 

    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete():
    ListaSpesa.query.delete() 
    db.session.commit() 

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)