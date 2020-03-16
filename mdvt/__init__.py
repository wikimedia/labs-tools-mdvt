from flask import Flask

from mdvt.main.route import main

app = Flask(__name__)
app.register_blueprint(main)
