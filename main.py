from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import secrets
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] =  secrets.token_hex(16) 
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"

with app.app_context():
    db.create_all()
 
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description', '')

    if not title:
        flash("Title is required!", "error")
        return redirect(url_for('index'))

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('index'))

@app.route('/toggle_done/<int:id>')
def toggle_done(id):
    task = Task.query.get_or_404(id)
    task.done = not task.done  
    db.session.commit()
    flash("Task updated successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
 
