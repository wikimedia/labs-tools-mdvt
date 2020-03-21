from flask import Blueprint, jsonify, render_template, request, session

from mdvt.contribute.util import get_contrib_request

contribute_bp = Blueprint('contribute', __name__)


@contribute_bp.route('/contribute')
def contribute():
    # filter_type = request.args.get('filter-type', 'recent')
    # if filter_type == 'recent':
    #     filter_value = ''
    # elif filter_type == 'category':
    #     filter_value = request.args.get('category')
    # elif filter_type == 'tag':
    #     filter_value = request.args.get('tag')

    return render_template('contribute/contribute.html',
                           title='Contribute',
                           username=session.get('username', None))


@contribute_bp.route('/api/get-media')
def api_get_media():
    filter_type = request.args.get('filter_type', 'recent')
    if filter_type == 'recent':
        return jsonify(get_contrib_request(filter_type, None))
    elif filter_type == 'category':
        return jsonify(get_contrib_request(filter_type,
                                           request.args.get('filter_value')))
    elif filter_type == 'tag':
        request.args.get('filter_value')
