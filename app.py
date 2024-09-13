from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the database and table
with app.app_context():
    db.create_all()


# In-memory database to store tasks
task = []
next_id = 1

@app.route('/')
def index():
    tasks = Task.query.all()  # Get all tasks from the database
    return render_template('index.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.json
        task = Task(name=data['name'], description=data['description'])
        db.session.add(task)
        db.session.commit()
        return jsonify({
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'completed': task.completed
        }), 201
    
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'name': task.name,
        'description': task.description,
        'completed': task.completed
    } for task in tasks])    
    
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    return '', 404

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'completed': task.completed
        })
    return '', 404

if __name__ == '__main__':
    app.run(debug=True)