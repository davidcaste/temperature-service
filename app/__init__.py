from flask import Flask

app = Flask(__name__)
from app import views

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs