from flask import Flask

from mdvt.config.config import config
from mdvt.main.route import main

app = Flask(__name__)

app.config['SECRET_KEY'] = config['SECRET_KEY']

app.register_blueprint(main)
