from flask import Flask

from . import settings

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = settings.SECRET_KEY

