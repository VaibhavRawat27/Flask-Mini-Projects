from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# -------------------- MODELS --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    scheduled_time = db.Column(db.DateTime, nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    now = datetime.utcnow()
    posts = BlogPost.query.filter(
        (BlogPost.is_published == True) | ((BlogPost.scheduled_time != None) & (BlogPost.scheduled_time <= now))
    ).order_by(BlogPost.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()
    if request.method == 'POST':
        content = request.form['comment']
        new_comment = Comment(post_id=post_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=post, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid Credentials!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return render_template('admin_dashboard.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        content = request.form['content']
        scheduled_time = request.form.get('scheduled_time')
        is_published = True if request.form.get('publish_now') else False

        schedule_dt = None
        if scheduled_time:
            schedule_dt = datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M')

        new_post = BlogPost(
            title=title, summary=summary, content=content,
            is_published=is_published, scheduled_time=schedule_dt
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('create_post.html')

@app.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
