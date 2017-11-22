# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import telebot
import config

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

token = config.token
bot = telebot.TeleBot(token)


class Activation(db.Model):
    __tablename__ = 'activation'
    id = db.Column(db.Integer, primary_key=True)
    machineid = db.Column(db.String(80), nullable=False)
    active = db.Column(db.SmallInteger, nullable=False, default=1)
    db_cred = db.Column(db.Text, nullable=False, default='')

    def __repr__(self):
        return '<machineid %r>' % self.machineid

def get_status(id):
    try:
        lic = Activation.query.filter_by(machineid=id, active=1).first()
        res = '' if not lic or not lic.active else lic.db_cred
    except Exception as e:
        res = e
    return res

def send_activation_query(id):
    try:
        res = '0'
        if id:
            for b in config.chat_ids.split(','):
                bot.send_message(b, u'Запрос активации ИС остатки для %s' % id)
    except Exception as e:
        res = e
    return res

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/active', methods=['POST'])
def active():
    if request.method == 'POST':
        status = get_status(request.form['machineid'])
    return status

@app.route('/activation', methods=['POST'])
def activation():
    if request.method == 'POST':
        status = send_activation_query(request.form['machineid'])
    return status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
