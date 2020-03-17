from flask import Blueprint, jsonify, render_template, request, session
import requests

from mdvt.contribute.util import get_contrib_request

contribute_bt = Blueprint('contribute', __name__)


@contribute_bt.route('/contribute')
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


@contribute_bt.route('/api/get-media')
def api_get_media():
    filter_type = request.args.get('filter-type', 'recent')
    if filter_type == 'recent':
        return jsonify(get_contrib_request())
    elif filter_type == 'category':
        category_members = requests.get(
            'https://commons.wikimedia.org/w/api.php',
            params={
                'action': 'query',
                'format': 'json',
                'list': 'allimages',
                'aisort': 'timestamp',
                'aidir': 'descending',
                'ailimit': 100
            }
        ).json()['query']['allimages']
        return jsonify([category_member['title']
                       for category_member in category_members])
    elif filter_type == 'tag':
        request.args.get('filter-value')
