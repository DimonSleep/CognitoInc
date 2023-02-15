from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

class ChatForm(FlaskForm):
    username = StringField('Username')
    message = StringField('Message')
    submit = SubmitField('Send')

class FileForm(FlaskForm):
    upload = photos
    submit = SubmitField('Upload')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    form = ChatForm()
    return render_template('chat.html', form=form)

@app.route('/file')
def file():
    form = FileForm()
    return render_template('file.html', form=form)

@app.route('/videochat')
def videochat():
    return render_template('videochat.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'username': 'System', 'message': 'Client connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    emit('message', {'username': 'System', 'message': 'Client disconnected'})

@socketio.on('message')
def handle_message(data):
    print('Received message: ' + data['message'])
    emit('message', data)

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True, include_self=False)

@socketio.on('candidate')
def handle_candidate(data):
    emit('candidate', data, broadcast=True, include_self=False)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = FileForm()
    if request.method == 'POST' and 'upload' in request.files:
        filename = photos.save(request.files['upload'])
        return 'File uploaded successfully'
    return render_template('file.html', form=form)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
