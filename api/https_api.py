import logging
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Logging configuration
logging.basicConfig(
    filename='https_api.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

with app.app_context():
    db.create_all()

# Credentials for Basic Auth
USERNAME = 'admin'
PASSWORD = 'password'

# Authentication decorator
def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            logger.warning(f"Unauthorized access attempt from IP: {request.remote_addr}")
            return make_response(jsonify({"message": "Authentication required"}), 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
        logger.info(f"Authorized access by user '{auth.username}' to {request.method} {request.path}")
        return f(*args, **kwargs)
    return decorated

@app.route('/users', methods=['GET'])
@basic_auth_required
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    logger.info("Fetched all users.")
    return jsonify({"users": users_list}), 200

@app.route('/users', methods=['POST'])
@basic_auth_required
def add_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        logger.error(f"Invalid data provided for user creation: {data}")
        return jsonify({"message": "Invalid data. 'name' and 'email' are required."}), 400

    new_user = User(name=data['name'], email=data['email'])
    try:
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"User added successfully: {data['name']} ({data['email']})")
        return jsonify({"message": "User added successfully.", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding user: {e}")
        return jsonify({"message": "Error adding user.", "error": str(e)}), 500

@app.route('/users', methods=['PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def method_not_allowed_users():
    logger.warning(f"Method not allowed: {request.method} {request.path}")
    return jsonify({"message": "Method not allowed"}), 405

# Run HTTPS server
if __name__ == '__main__':
    logger.info("Starting HTTPS server...")
    app.run(host='0.0.0.0', port=443, ssl_context=(r'cert.pem', r'key.pem'), debug=True)
