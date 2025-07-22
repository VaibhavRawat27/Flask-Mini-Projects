import os
import uuid
import base64
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["USER_PHOTOS"] = "static/user_photos"
socketio = SocketIO(app)
app.secret_key = "supersecret"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])
if not os.path.exists(app.config["USER_PHOTOS"]):
    os.makedirs(app.config["USER_PHOTOS"])

DB_NAME = "database.db"

# ------------------ Database Setup ------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS polls (
        id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        image TEXT,
        image_caption TEXT,
        options TEXT,
        end_time TEXT,
        admin TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_id TEXT,
        name TEXT,
        gender TEXT,
        email TEXT,
        phone TEXT,
        location TEXT,
        option TEXT,
        photo TEXT,
        timestamp TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')

    # Insert default admin if not exists
    c.execute("SELECT * FROM admins WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO admins (username,password) VALUES (?,?)", ("admin", "admin123"))

    conn.commit()
    conn.close()

init_db()

# ------------------ Helper Functions ------------------
def get_poll(poll_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM polls WHERE id=?", (poll_id,))
    poll = c.fetchone()
    conn.close()
    return poll

def get_votes(poll_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM votes WHERE poll_id=?", (poll_id,))
    votes = c.fetchall()
    conn.close()
    return votes

def poll_expired(end_time):
    return datetime.now() > datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

def time_left(end_time):
    dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    diff = dt - datetime.now()
    if diff.total_seconds() <= 0:
        return "Ended"
    return str(diff).split('.')[0]  # HH:MM:SS

def get_all_polls():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM polls")
    polls = c.fetchall()
    conn.close()
    return polls

# ------------------ Routes ------------------
@app.route("/")
def index():
    polls = get_all_polls()
    active, past = [], []

    for p in polls:
        timeleft = time_left(p[6])  # Use the helper we already created
        poll_with_time = list(p) + [timeleft]

        if poll_expired(p[6]):
            past.append(poll_with_time)
        else:
            active.append(poll_with_time)

    return render_template("index.html", active=active, past=past)

@app.route("/create_poll", methods=["GET", "POST"])
def create_poll():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        options = request.form.getlist("options[]")
        hours = int(request.form["hours"])

        image_file = request.files["image"]
        image_filename = ""
        if image_file.filename:
            image_filename = f"{uuid.uuid4().hex}_{image_file.filename}"
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        image_caption = request.form["image_caption"]
        poll_id = uuid.uuid4().hex[:6]
        end_time = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO polls (id,title,description,image,image_caption,options,end_time,admin) VALUES (?,?,?,?,?,?,?,?)",
                  (poll_id, title, description, image_filename, image_caption, "|".join(options), end_time, session["admin"]))
        conn.commit()
        conn.close()

        return redirect(url_for("admin_dashboard"))
    return render_template("create_poll.html")

@app.route("/vote/<poll_id>", methods=["GET", "POST"])
def vote(poll_id):
    poll = get_poll(poll_id)
    if not poll:
        return "Poll does not exist!", 404

    if poll_expired(poll[6]):
        return render_template("results.html", poll_id=poll_id)

    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        location = request.form["location"]
        option = request.form["option"]
        photo_data = request.form["photo"]

        filename = f"{uuid.uuid4().hex}.png"
        if photo_data:
            photo_data = photo_data.split(",")[1]
            with open(os.path.join(app.config["USER_PHOTOS"], filename), "wb") as f:
                f.write(base64.b64decode(photo_data))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO votes (poll_id,name,gender,email,phone,location,option,photo,timestamp) VALUES (?,?,?,?,?,?,?,?,?)",
                  (poll_id, name, gender, email, phone, location, option, filename, timestamp))
        conn.commit()
        conn.close()

        socketio.emit("update_results", get_results_data(poll_id), to=poll_id)
        return render_template("vote_success.html", poll_id=poll_id)
    return render_template("vote.html", poll=poll, time_left=time_left(poll[6]))

@app.route("/results/<poll_id>")
def results(poll_id):
    poll = get_poll(poll_id)
    if not poll:
        return "Poll does not exist!", 404
    return render_template("results.html", poll_id=poll_id)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()
        if admin:
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid login!"
    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    
    polls = get_all_polls()
    my_polls = []

    for p in polls:
        if p[7] == session["admin"]:
            poll_with_time = list(p) + [time_left(p[6])]
            my_polls.append(poll_with_time)

    return render_template("admin_dashboard.html", polls=my_polls)


@app.route("/admin/<poll_id>")
def admin_view(poll_id):
    votes = get_votes(poll_id)
    return render_template("admin.html", votes=votes, poll_id=poll_id)

# ------------------ API ------------------
@app.route("/api/results/<poll_id>")
def api_results(poll_id):
    return jsonify(get_results_data(poll_id))

def get_results_data(poll_id):
    poll = get_poll(poll_id)
    if not poll:
        return {}
    options = poll[5].split("|")
    votes = get_votes(poll_id)
    counts = {opt: 0 for opt in options}
    gender_counts = {"Male": 0, "Female": 0, "Other": 0}
    for v in votes:
        counts[v[7]] += 1
        gender_counts[v[3]] += 1
    total = len(votes)
    percentages = {opt: (counts[opt] / total * 100 if total else 0) for opt in counts}
    return {"options": counts, "percentages": percentages, "gender": gender_counts, "total": total}

@socketio.on("join")
def on_join(data):
    poll_id = data["poll_id"]
    join_room(poll_id)
    emit("update_results", get_results_data(poll_id), to=poll_id)

if __name__ == "__main__":
    socketio.run(app, debug=True)
