from flask.ext.mongoengine import MongoEngine

db = MongoEngine()
import datetime

class User(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    username = db.StringField(max_length=255)
    github_access_token = db.StringField(max_length=64, required=True)

    def __unicode__(self):
        return self.github_access_token

    meta = {
        'indexes': ['-created_at']
    }


class Hook(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    repo_id = db.IntField(required=True)
    username = db.StringField(max_length=255, required=True)

    def __unicode__(self):
        return 'Hook for repo #{}'.format(self.repo_id)

    meta = {
        'indexes': ['-created_at', 'repo_id']
    }
