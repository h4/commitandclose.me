from flask import render_template, session, redirect, url_for, request
from . import main
from flask.ext.github import GitHub

github = GitHub()
auth_scopes = 'write:repo_hook,repo'


@main.route('/')
def index():
    return render_template('app/index.html')


@main.route('/profile')
def profile():
    if session.get('user_id', None) is None:
        return redirect(url_for('.login'))
    return render_template('app/profile.html')


@main.route('/authorise')
@github.authorized_handler
def authorized(access_token):
    # next_url = request.args.get('next') or url_for('index')
    # if access_token is None:
    #     return redirect(next_url)

    # user = User.query.filter_by(github_access_token=access_token).first()
    # if user is None:
    #     user = User(access_token)
    #     db_session.add(user)
    # user.github_access_token = access_token
    # db_session.commit()

    # session['user_id'] = user.id
    session['access_token'] = access_token
    return redirect(url_for('.index'))


@main.route('/profile/repos')
def repos():
    result = github.get('user/repos')
    return str(result)


@main.route('/profile/addhook')
def add_hook():
    hook_data = {
        "name": "web",
        "active": True,
        "events": [
            "push",
            "pull_request"
        ],
        "config": {
            "url": "http://commitandclose.me/hook",
            "content_type": "json"
        }
    }
    result = github.post('repos/h4/commitandclose.me/hooks', hook_data)
    # result = github.get('repos/h4/commitandclose.me')
    return str(result)
    # return render_template('add_hook.html')


@main.route('/profile/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize(scope=auth_scopes)
    return redirect(url_for('profile'))


@main.route('/profile/issue')
def issue():
    issue_data = {
        "state": "closed"
    }
    github.post('repos/h4/commitandclose.me/issues/1/comments', {
        "body": "Closed via http://commitandclose.me/ by commit SHA"
    })
    result = github.post('repos/h4/commitandclose.me/issues/1', issue_data)
    return str(result)


@main.route('/hook', methods=['POST'])
def hook():
    payload = request.json
    commits = payload['commits']
    print(commits)
    return render_template('app/hook.html')
