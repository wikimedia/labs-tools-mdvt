from flask import (Blueprint, jsonify, render_template, redirect, request,
                   session, url_for)

from mdvt.contribute.util import get_contrib_request
from mdvt.database.util import db_set_or_update_user_setting
from mdvt.main.util import is_logged_in

contribute_bp = Blueprint('contribute', __name__)


@contribute_bp.route('/contribute')
def contribute():
    if not is_logged_in():
        return redirect(url_for('main.login'))

    filter_type = request.args.get('filter-type', 'recent')
    db_set_or_update_user_setting(session.get('user_id'),
                                  'filter_type',
                                  filter_type)

    filter_category = request.args.get('category')
    if filter_category:
        db_set_or_update_user_setting(session.get('user_id'),
                                      'filter_category',
                                      filter_category)

    filter_tag = request.args.get('tag').replace('_', ' ')
    if filter_tag:
        db_set_or_update_user_setting(session.get('user_id'),
                                      'filter_tag',
                                      filter_tag)

    return render_template('contribute/contribute.html',
                           title='Contribute',
                           username=session.get('username', None))


@contribute_bp.route('/api/get-media')
def api_get_media():
    filter_type = request.args.get('filter_type', 'recent')
    if filter_type == 'recent':
        filter_value = None
    elif filter_type == 'category':
        filter_value = request.args.get('filter_value')
    else:
        filter_value = request.args.get('filter_value').replace('_', ' ')

    return jsonify(get_contrib_request(filter_type, filter_value))
