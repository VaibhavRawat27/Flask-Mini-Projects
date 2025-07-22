from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="To Do")  # To Do, In Progress, Done
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/')
def index():
    tasks = Task.query.all()
    todo = [t for t in tasks if t.status == "To Do"]
    progress = [t for t in tasks if t.status == "In Progress"]
    done = [t for t in tasks if t.status == "Done"]
    return render_template('index.html', todo=todo, progress=progress, done=done)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    priority = request.form.get('priority', 'Medium')
    due_date = request.form.get('due_date')
    new_task = Task(title=title, priority=priority, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    task = Task.query.get(data['task_id'])
    if task:
        task.status = data['status']
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
