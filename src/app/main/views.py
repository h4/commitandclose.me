import re
from app.models import User
from flask import g, render_template, session, redirect, url_for, request
from . import main
from flask.ext.github import GitHub

github = GitHub()
auth_scopes = 'write:repo_hook,repo'


def get_pages(response):
    re_rel = re.compile('^rel=\"([a-z]+)\"$')
    re_page = re.compile('page=([0-9]+)')
    links = [item.split('; ') for item in response.headers['Link'].split(', ')]
    links_dict = {}
    for item in links:
        links_dict[re_rel.findall(item[1])[0]] = re_page.findall(item[0])[0]

    return links_dict


def get_all_repos(github):
    response = github.raw_request('get', 'user/repos')
    status_code = str(response.status_code)

    if not status_code.startswith('2'):
        return []
    repos = response.json()
    pages = get_pages(response)
    if 'last' in pages:
        for page in range(1, int(pages['last'])):
            repos += github.raw_request('get', 'user/repos', {'page': page + 1}).json()
    return repos


@main.route('/')
def index():
    user = User.objects(github_access_token=session.get('access_token', None)).first()
    return render_template('app/index.html', user=user)


@main.route('/profile')
def profile():
    if session.get('access_token', None) is None:
        return redirect(url_for('.login'))
    orgs = github.get('user/orgs')
    repos = get_all_repos(github)
    return render_template('app/profile.html', repos=repos, orgs=orgs)


@main.route('/authorise')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('.index')
    if access_token is None:
        return redirect(next_url)

    user = User.objects(github_access_token=access_token).first()
    if user is None:
        user = User(github_access_token=access_token)
        user.save()

    session['access_token'] = access_token

    if user.username is None:
        g.user = user
        user_data = github.get('user')
        user.username = user_data.get('login', None)
        user.save()
    #     db_session.add(user)
    # user.github_access_token = access_token
    # db_session.commit()

    # session['user_id'] = user.id
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


@main.route('/profile/logout')
def logout():
    del session['access_token']
    return redirect(url_for('.index'))


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
