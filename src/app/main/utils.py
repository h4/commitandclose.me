from . import main
from flask import g, session
from app.models import User
from .views import github

@main.before_request
def before_request():
    g.user = None
    if 'access_token' in session:
        g.user = User(session['access_token'])


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token
