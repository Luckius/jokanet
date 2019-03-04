from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sql9278732:3aLTCvgXjf@sql9.freemysqlhosting.net/sql9278732"
db = SQLAlchemy(app)


class Chathistory(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    allmessage = db.Column('allmessage', db.String(500))
    mymessage = db.Column('mymessage', db.String(500))
    userusername = db.Column('userusername', db.String(50))

users = {}

@app.route('/')
def index():
    allmessages = Chathistory.query.all()
    return render_template('index.html',allmessages=allmessages)

@app.route('/orginate')
def orginate():
    socketio.emit('server orginated', 'Something happened on the server!')
    return '<h1>Sent!</h1>'

@socketio.on('message from user', namespace='/messages')
def receive_message_from_user(message):
    print('USER MESSAGE: {}'.format(message))
    allmessage = Chathistory(allmessage=message)
    db.session.add(allmessage)
    db.session.commit()
    emit('from flask', message.upper(), broadcast=True)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users[username] = request.sid
    userusername = Chathistory(userusername=username)
    db.session.add(userusername)
    db.session.commit()
    #users.append({username : request.sid})
    #print(users)
    print('Username added!')



@socketio.on('private_message', namespace='/private')
def private_message(payload):
    recipient_session_id = users[payload['username']]
    message = payload['message']
    emit('new_private_message',message, room=recipient_session_id)



if __name__ == '__main__':
    socketio.run(app)