from flask import Flask

from mdvt.config.config import config
from mdvt.contribute.route import contribute_bt
from mdvt.main.route import main_bt

app = Flask(__name__)

app.config['SECRET_KEY'] = config['SECRET_KEY']

app.register_blueprint(main_bt)
app.register_blueprint(contribute_bt)
