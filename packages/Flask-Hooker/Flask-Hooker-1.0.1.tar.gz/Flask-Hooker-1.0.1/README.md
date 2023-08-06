#Flask-Hooker
Receive and manage webhooks of several services at the same time

###Simple usage
```python 
from flask import Flask
from flask_hooker import Hooker

def github_issue(json):
    print 'new issue at:', json['issue']['url']
    
def gitlab_push(json):
    print 'the user %s push change into %s' % (json['user_name'], json['project']['name'])

app = Flask(__name__)

hooker = Hooker(app=app, url_prefix='/webhook')

# with fabrics
# hooker = Hooker()
# hooker.init_app(app)

hooker.add_handler(event='issues', func=github_issue, event_type='X-Github-Event')
hooker.add_handler('Push Hook', gitlab_push, 'X-Gitlab-Event')

...
```
