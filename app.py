from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from passlib.hash import bcrypt

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'  
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User(name:{self.name}, email:{self.email}, role:{self.role})"

    def hash_password(self, password):
        self.password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)


# Request parser for registration
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="Name of the user is required", required=True)
user_post_args.add_argument("email", type=str, help="Email of the user is required", required=True)
user_post_args.add_argument("password", type=str, help="Password of the user is required", required=True)
user_post_args.add_argument("role", type=str, help="Role of the user is required", required=True)

# Register new user
class Register(Resource):
    def post(self):
        args = user_post_args.parse_args()
        if UserModel.query.filter_by(email=args['email']).first():
            abort(409, message="User with this email already exists.")
        
        new_user = UserModel(
            name=args['name'], 
            email=args['email'], 
            role=args['role']
        )
        new_user.hash_password(args['password'])
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="User registered successfully!")

# Login User and return JWT token
class Login(Resource):
    def post(self):
        login_args = reqparse.RequestParser()
        login_args.add_argument("email", type=str, help="Email is required", required=True)
        login_args.add_argument("password", type=str, help="Password is required", required=True)
        args = login_args.parse_args()

        user = UserModel.query.filter_by(email=args['email']).first()
        if not user or not user.verify_password(args['password']):
            abort(401, message="Invalid credentials")
        
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)

# Protected endpoint to get user profile
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }

# Request parser for updating user profile
user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="Name of the user")
user_update_args.add_argument("email", type=str, help="Email of the user")
user_update_args.add_argument("role", type=str, help="Role of the user")

# Update user profile
class UpdateProfile(Resource):
    @jwt_required()
    def put(self):
        args = user_update_args.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        
        if not user:
            abort(404, message="User not found")
        
        # Update fields if provided
        if args['name']:
            user.name = args['name']
        if args['email']:
            # Ensure that the new email is not already taken by another user
            if UserModel.query.filter_by(email=args['email']).first():
                abort(409, message="Email already in use")
            user.email = args['email']
        if args['role']:
            user.role = args['role']
        
        db.session.commit()
        return jsonify(message="User profile updated successfully!")

# Add resources for the API (API Endpoints)
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(UserProfile, '/profile')
api.add_resource(UpdateProfile, '/profile/update')

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # This ensures that the database tables are created within the app context
    app.run(debug=True)



