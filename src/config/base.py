import os


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    GITHUB_CLIENT_ID = '7e1c8e03adace91dd408'
    GITHUB_CLIENT_SECRET = 'ed4d777cde8decf56b025b2185aefdb6c4a311bd'
    GITHUB_CALLBACK_URL = 'http://commitandclose.h404.ru/authorise'
    MONGODB_DB = 'commitandclose'
    # MONGODB_USERNAME = 'h4'
    # MONGODB_PASSWORD = 'password'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 0

    @staticmethod
    def init_app(app):
        pass
