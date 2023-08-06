#Flask-Hooker
Receive and manage webhooks of several services at the same time

[![PyPI version](https://badge.fury.io/py/Flask-Hooker.svg)](https://badge.fury.io/py/Flask-Hooker)
[![Build Status](https://travis-ci.org/doblel/Flask-Hooker.svg?branch=master)](https://travis-ci.org/doblel/Flask-Hooker)
[![Code Health](https://landscape.io/github/doblel/Flask-Hooker/master/landscape.svg?style=flat)](https://landscape.io/github/doblel/Flask-Hooker/master)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/doblel/Flask-Hooker/issues)


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
