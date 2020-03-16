from flask import Blueprint, render_template, session

contribute_bt = Blueprint('contribute', __name__)


@contribute_bt.route('/contribute', defaults={'type': 'depict'})
@contribute_bt.route('/contribute/<string:type>')
def contribute(type):
    return render_template('contribute/contribute.html',
                           title='Contribute',
                           username=session.get('username', None))
