from flask import Flask, render_template, request, redirect, url_for  #Importa i moduli necessari di Flask
from flask_sqlalchemy import SQLAlchemy  #Importa SQLAlchemy
from moduls import db, ListaSpesa  #Importa il database e il modello ListaSpesa da un modulo separato

#Crea l'applicazione Flask
app = Flask(__name__)

#Configurazione del database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista_spesa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inizializza SQLAlchemy con l'app
db.init_app(app)

#Creazione delle tabelle del database
with app.app_context():
    db.create_all() 

#Creazione lista
lista_spese = []

#Dichiarazione root iniziale
@app.route('/')
def home():
    lista_spesa = ListaSpesa.query.all()
    return render_template('index.html', lista_spese=lista_spesa)

#Dichiarazione root per aggiungere elementi
@app.route('/add', methods=['POST'])
def add():
    elemento = request.form['elemento'] 
    if elemento:  
        nuovo_elemento = ListaSpesa(elemento=elemento)
        db.session.add(nuovo_elemento)
        db.session.commit()
    return redirect(url_for('home'))

#Dichiarazione root per rimuovere elementi singoli
@app.route('/remove/<int:indice>', methods=['POST'])
def remove(indice):
    elemento = ListaSpesa.query.get_or_404(indice)
    db.session.delete(elemento)
    db.session.commit()
    return redirect(url_for('home'))

#Dichiarazione root per eliminare tutti gli elementi presenti nella lista
@app.route('/delete', methods=['POST'])
def delete():
    ListaSpesa.query.delete()
    db.session.commit()
    return redirect(url_for('home'))

#Avvio dell'applicazione
if __name__ == '__main__':
    app.run(debug=True)
