# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Activation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machineid = db.Column(db.String(80), nullable=False)
    active = db.Column(db.SmallInteger, nullable=False, default=1)

    def __repr__(self):
        return '<machineid %r>' % self.machineid

def get_status(id):
    lic = Activation.query.filter_by(machineid=id).first()
    return lic or lic.active

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/active', methods=['POST'])
def active():
    if request.method == 'POST':
        status = get_status(request.form('machineid'))
    return status


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
