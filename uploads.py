import pusher
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sql9278732:3aLTCvgXjf@sql9.freemysqlhosting.net/sql9278732"


pusher_client = pusher.Pusher(
  app_id='712449',
  key='1ed944948aaacb0d5e85',
  secret='be9f14f96b374cfc0684',
  cluster='ap2',
  ssl=True
)



db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))


@app.route('/')
def index():
    messages = Message.query.all()

    return render_template('test.html', messages=messages)


@app.route('/message', methods=['POST'])
def message():
    try:

        username = request.form.get('username')
        message = request.form.get('message')

        new_message = Message(username=username, message=message)
        db.session.add(new_message)
        db.session.commit()

        pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})

        return jsonify({'result': 'success'})

    except:

        return jsonify({'result': 'failure'})


if __name__ == '__main__':
    app.run(debug=True)