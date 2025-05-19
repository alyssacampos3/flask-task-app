# Import necessary modules from Flask and SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy without an app context
db = SQLAlchemy()

# Define the Task model representing a task in the database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each task
    title = db.Column(db.String(80), nullable=False)  # Title of the task
    completed = db.Column(db.Boolean, default=False)  # Completion status
    
    @classmethod
    '''
    def find_by_title(cls, title):
        """
        Class method to find a task by its title.
        """
        return cls.query.filter_by(title=title).first()
    Made initially before figuring out a more optimized way to delete.
    Could still be useful in the future./
    '''
    def to_dict(self):
        """
        Convert the Task object into a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

def create_app():
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'  # Database configuration
    db.init_app(app)  # Initialize the app with SQLAlchemy

    @app.route('/tasks', methods=['POST'])
    def add_task():
        """
        Endpoint to add a new task.
        Expects JSON data with a 'title' field.
        """
        task_data = request.get_json()
        new_task = Task(title=task_data['title'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'title': new_task.title}), 200

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        """
        Endpoint to retrieve all tasks.
        """
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(title):
        """
        Endpoint to delete a task.
        """
        task = Task.query.get_or_404(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()
        return '', 204

    @app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
    def complete_task(task_id):
        """
        Endpoint to mark a task as completed by its ID.
        """
        task = Task.query.get_or_404(task_id)
        task.completed = True
        db.session.commit()
        return jsonify(task.to_dict()), 200

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """
        Endpoint to update the title of a task by its ID.
        Expects JSON data with a 'title' field.
        """
        task = Task.query.get_or_404(task_id)
        data = request.get_json()

        if 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400

        task.title = data['title']
        db.session.commit()
        return jsonify(task.to_dict()), 200

    @app.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """
        Endpoint to retrieve a single task by its ID.
        """
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict()), 200

    return app

# Entry point to run the Flask application
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the app in debug mode
