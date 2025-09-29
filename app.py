from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Task, NGO, User, Signup
from config import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, origins=["*"])

    # Seed database if empty
    with app.app_context():
        db.create_all()
        if NGO.query.count() == 0:
            print("Database is empty, seeding with mock data...")
            from seed_data import seed_if_empty
            seed_if_empty()
            print("Seeding completed.")
        else:
            print("Database already has data, skipping seed.")

    # Root route
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({'message': 'Welcome to the Volunteer API'})

    # API Routes
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route('/api/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        # For now, assume ngo_id is provided or default
        ngo_id = data.get('ngo_id', 1)  # Default to first NGO
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        from datetime import datetime
        due_date = datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None
        task = Task(
            ngo_id=ngo_id,
            user_id=user_id,
            title=data['title'],
            description=data.get('description'),
            category=data.get('category', 'general'),
            location=data['location'],
            hours=data['hours'],
            due_date=due_date
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @app.route('/api/signups', methods=['POST'])
    def volunteer_for_task():
        data = request.get_json()
        task_id = data.get('task_id')
        user_id = data.get('user_id')
        message = data.get('message', '')
        if not task_id or not user_id:
            return jsonify({'error': 'task_id and user_id required'}), 400
        # Check if task exists
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        # Check if already signed up
        existing_signup = Signup.query.filter_by(task_id=task_id, user_id=user_id).first()
        if existing_signup:
            return jsonify({'error': 'Already volunteered for this task'}), 400
        signup = Signup(task_id=task_id, user_id=user_id, message=message)
        db.session.add(signup)
        db.session.commit()
        return jsonify(signup.to_dict()), 201

    @app.route('/api/task-signups', methods=['GET', 'POST'])
    def task_signups():
        if request.method == 'GET':
            signups = Signup.query.all()
            return jsonify([signup.to_dict() for signup in signups])
        elif request.method == 'POST':
            data = request.get_json()
            task_id = data.get('task_id')
            user_id = data.get('user_id')
            message = data.get('message', '')
            if not task_id or not user_id:
                return jsonify({'error': 'task_id and user_id required'}), 400
            # Check if task exists
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            # Check if already signed up
            existing_signup = Signup.query.filter_by(task_id=task_id, user_id=user_id).first()
            if existing_signup:
                return jsonify({'error': 'Already volunteered for this task'}), 400
            signup = Signup(task_id=task_id, user_id=user_id, message=message)
            db.session.add(signup)
            db.session.commit()
            return jsonify(signup.to_dict()), 201

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.password == data['password']:
            return jsonify({'message': 'Login successful', 'user': user.to_dict()})
        return jsonify({'error': 'Invalid credentials'}), 401

    @app.route('/api/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        user = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Signup successful', 'user': user.to_dict()}), 201

    @app.route('/api/admin/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route('/api/admin/signups', methods=['GET'])
    def get_signups():
        signups = Signup.query.all()
        return jsonify([signup.to_dict() for signup in signups])

    @app.route('/api/admin/data', methods=['GET'])
    def get_admin_data():
        tasks_count = Task.query.count()
        users_count = User.query.count()
        signups_count = Signup.query.count()
        return jsonify({
            'tasks': tasks_count,
            'users': users_count,
            'signups': signups_count
        })


    @app.errorhandler(404)
    def not_found(error):
        print(f"404 Error: Requested URL: {request.url}, Method: {request.method}")
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create app instance for Flask CLI
app = create_app()

# This allows us to use this file with Flask CLI commands
if __name__ == '__main__':
    print("Starting Flask app on host=0.0.0.0, port=5000, debug=True")
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
