from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template
from flask_socketio import SocketIO, send


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sql10278488:VAqQEV2rvy@sql10.freemysqlhosting.net/sql10278488"
db = SQLAlchemy(app)


class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(500))


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    message = History(message=msg)
    db.session.add(message)
    db.session.commit()
    send(msg, broadcast=True)

@app.route('/')
def index():
    messages = History.query.all()
    return render_template('chatting.html', messages=messages)


if __name__ == '__main__':
    socketio.run(app,debug=True)



