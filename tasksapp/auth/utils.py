from tasksapp.models import User
from flask_jwt_extended import  create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

# Register user
class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
    
    def post(self):
        self.parser.add_argument('name', type=str, required=True, help='Name is required')
        self.parser.add_argument('email', type=str, required=True, help='Email is required')
        self.parser.add_argument('password', type=str, required=True, help='Password is required')

        user_data = self.parser.parse_args()

        if User.find_user_by_email(user_data['email']):
            return {'message': 'User with {} already exists'.format(user_data['email'])}, 400

        new_user = User(
            name=user_data['name'],
            email=user_data['email'],
            password=User.hash_password(user_data['password'])
        )
        new_user.save()
        return {'message': 'User {} was created'.format(user_data['email'])}, 201

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def Post(self):
        self.parser.add_argument('email', type=str, required=True, help='Email required')
        self.parser.add_argument('password', type=str, required=True, help='Password is required')
        postdata = self.parser.parse_args()

        #get user detail
        user_detail = User.find_user_by_email(postdata['email'])

        #if user exists and passord is verified, then create access and refresh tokens for user
        if user_detail and User.verify_hash(postdata['password'], user_detail.password):
            api_user_identity = {'id':user_detail.id, 'name': user_detail.name}
            access_token = create_access_token(identity=api_user_identity)
            refresh_token = create_refresh_token(identity=api_user_identity)
            return {
                'access_token': access_token, 
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Invalid login credentials supplied'}, 401


