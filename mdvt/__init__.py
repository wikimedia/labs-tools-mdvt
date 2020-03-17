from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from mdvt.config.config import config
from mdvt.contribute.route import contribute_bt
from mdvt.main.route import main_bt

app = Flask(__name__)

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
db = SQLAlchemy(app)

app.register_blueprint(main_bt)
app.register_blueprint(contribute_bt)
