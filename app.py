from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

with app.app_context():
    db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # creates int id for each task
    content = db.Column(db.String(200), nullable=False) # Task with 200 characters, and no empty tasks allowed
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # date of task creation

    def __repr__(self):
        ### returns the task's id
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])   # Route decorator
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # input tag with name=content
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()   # looks at all created tasks, sorts by date and returns the list
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem in updating the task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)