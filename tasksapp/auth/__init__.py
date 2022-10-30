from tasksapp.auth.utils import Login, Register

def auth_routes(api):
    api.add_resource(Login, '/tasks_api/login/')
    api.add_resource(Register, '/tasks_api/register')