from flask.ext.mongoengine import MongoEngine

db = MongoEngine()
import datetime

class User(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    username = db.StringField(max_length=255, required=True)
    github_access_token = db.StringField(max_length=64, required=True)

    def __unicode__(self):
        return self.github_access_token

    meta = {
        'indexes' : ['-created_at', 'facebook_id'],
        'ordering' : ['-created_at']
    }
