
from datetime import datetime, date
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(BASE_DIR / 'saude_conectada.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    goal = db.Column(db.String(255), nullable=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    minutes = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.Date, nullable=False, default=date.today)

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.Date, nullable=False, default=date.today)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def calc_points():
    points = 0
    for a in Activity.query.all():
        if a.type == 'exercicio':
            points += 10
        elif a.type == 'alimentacao':
            txt = (a.value or "").lower()
            if any(k in txt for k in ['salada','fruta','água','agua','integral','legume','verdura']):
                points += 2
    points += Mood.query.count()
    return points

def recommendations():
    recs = []
    today = date.today()
    if Activity.query.filter_by(type='exercicio', created_at=today).count() == 0:
        recs.append("Sem registro de exercício hoje: tente 20 minutos de caminhada.")
    last_food = Activity.query.filter_by(type='alimentacao').order_by(Activity.id.desc()).first()
    if not last_food or not any(k in (last_food.value or '').lower() for k in ['água','agua','fruta']):
        recs.append("Hidratação e fibras: registre ingestão de água e inclua uma fruta.")
    last_mood = Mood.query.order_by(Mood.id.desc()).first()
    if last_mood and last_mood.mood.lower() in ['cansado','triste','ansioso']:
        recs.append("Observe seu descanso: avalie reduzir intensidade e priorizar sono.")
    if not recs:
        recs.append("Ótimo ritmo! Mantenha constância e registre seus hábitos diariamente.")
    return recs

@app.route('/')
def index():
    u = User.query.first()
    pts = calc_points()
    return render_template('index.html', user=u, points=pts)

@app.route('/setup', methods=['GET','POST'])
def setup():
    u = User.query.first()
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age') or None
        weight = request.form.get('weight') or None
        goal = request.form.get('goal')
        if u is None:
            u = User(name=name, age=int(age) if age else None, weight=float(weight) if weight else None, goal=goal)
            db.session.add(u)
        else:
            u.name = name
            u.age = int(age) if age else None
            u.weight = float(weight) if weight else None
            u.goal = goal
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('setup.html', user=u)

@app.route('/log', methods=['GET','POST'])
def log_activity():
    if request.method == 'POST':
        atype = request.form.get('type')
        value = request.form.get('value')
        minutes = request.form.get('minutes') or None
        calories = request.form.get('calories') or None
        if atype not in ['exercicio','alimentacao']:
            flash('Tipo inválido.', 'danger')
            return redirect(url_for('log_activity'))
        a = Activity(
            type=atype,
            value=value,
            minutes=int(minutes) if minutes else None,
            calories=int(calories) if calories else None
        )
        db.session.add(a)
        db.session.commit()
        flash('Registro incluído!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('log.html')

@app.route('/mood', methods=['GET','POST'])
def mood():
    if request.method == 'POST':
        mood = request.form.get('mood')
        notes = request.form.get('notes')
        m = Mood(mood=mood, notes=notes)
        db.session.add(m)
        db.session.commit()
        flash('Humor registrado!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('mood.html')

@app.route('/dashboard')
def dashboard():
    acts = Activity.query.order_by(Activity.created_at.desc(), Activity.id.desc()).limit(20).all()
    moods = Mood.query.order_by(Mood.created_at.desc(), Mood.id.desc()).limit(10).all()
    recs = recommendations()
    pts = calc_points()
    return render_template('dashboard.html', activities=acts, moods=moods, recs=recs, points=pts)

@app.route('/community', methods=['GET','POST'])
def community():
    if request.method == 'POST':
        author = request.form.get('author') or 'Anônimo'
        content = request.form.get('content')
        if content and content.strip():
            db.session.add(Post(author=author.strip(), content=content.strip()))
            db.session.commit()
            flash('Mensagem publicada!', 'success')
        else:
            flash('Escreva algo antes de publicar.', 'warning')
        return redirect(url_for('community'))
    posts = Post.query.order_by(Post.created_at.desc()).limit(50).all()
    return render_template('community.html', posts=posts)

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("Banco inicializado.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
