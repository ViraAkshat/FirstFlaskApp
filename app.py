from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)        # creates int id for each task
    content = db.Column(db.String(200), nullable=False) # Task with 200 characters, and no empty tasks allowed
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # date of task creation

    def __repr__(self):
        ### returns the task's id
        return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)