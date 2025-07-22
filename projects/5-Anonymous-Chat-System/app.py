import os
import random, string
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
socketio = SocketIO(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Room data: { room_id: {"title": str, "desc": str, "users": []} }
rooms = {}

def generate_room_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    title = request.form.get("title", "Untitled Room")
    desc = request.form.get("desc", "")
    room_id = generate_room_id()
    rooms[room_id] = {"title": title, "desc": desc, "users": []}
    return redirect(url_for('room', room_id=room_id))

@app.route('/room/<room_id>')
def room(room_id):
    if room_id not in rooms:
        return "Room does not exist!", 404
    return render_template(
        'room.html',
        room_id=room_id,
        room_title=rooms[room_id]["title"],
        room_desc=rooms[room_id]["desc"]
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return {"file_url": f"/static/uploads/{filename}"}

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    if room in rooms and username not in rooms[room]["users"]:
        rooms[room]["users"].append(username)

    emit("user_list", rooms[room]["users"], to=room)
    send({"system": True, "msg": f"🔵 {username} joined the chat"}, to=room)

@socketio.on('message')
def handle_message(data):
    data["time"] = datetime.now().strftime("%d %b, %H:%M")  # e.g., 17 Jul, 15:42
    emit("message", data, to=data['room'])

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    if room in rooms and username in rooms[room]["users"]:
        rooms[room]["users"].remove(username)
    emit("user_list", rooms[room]["users"], to=room)
    send({"system": True, "msg": f"🔴 {username} left the chat"}, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
