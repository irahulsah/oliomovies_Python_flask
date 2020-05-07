from flask import Flask,render_template

from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] =''
    

db = SQLAlchemy(app)


class contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(13), nullable=False)
    Message = db.Column(db.String(100), nullable=False)
    Date = db.Column(db.String(40), nullable=True)

    def __init__(self, Name, Email, Phone, Message, Date):
        self.Name = Name
        self.Email = Email
        self.Phone = Phone  
        self.Message = Message 
        self.Date = Date

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacts' , methods = ['GET','POST'])
def contacts():

    if (request.method = 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(Name = name , Email = email , Phone = phone , Message = message , Date = datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('index.html')

if __name__ == "__main__":
 



app.run()