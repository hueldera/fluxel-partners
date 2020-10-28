
import environ

env = environ.Env()
environ.Env.read_env()

if env('ENVIROMENT') == 'development':
    print("//-- Development Enviroment --//")
    from core.settings_local import *
elif env('ENVIROMENT') == 'production':
    print("//-- Production Enviroment --//")
    from core.settings_production import *
