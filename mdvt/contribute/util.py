from flask import session

import requests
import secrets


def api_all_images(continue_key=None):
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'allimages',
        'aisort': 'timestamp',
        'aidir': 'descending',
        'ailimit': 100
    }

    if continue_key is not None:
        params['aicontinue'] = continue_key

    response = requests.get(
        'https://commons.wikimedia.org/w/api.php',
        params=params
    ).json()

    return (response['query']['allimages'],
            response['continue']['aicontinue'])


def api_category_members(category_name, continue_key=None):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'info',
        'generator': 'categorymembers',
        'inprop': 'url',
        'gcmtitle': category_name,
        'gcmnamespace': '14|6'
    }

    if continue_key is not None:
        params['gcmcontinue'] = continue_key

    response = requests.get(
        'https://commons.wikimedia.org/w/api.php',
        params=params
    ).json()

    return (list(response['query']['pages'].values()),
            response['continue']['gcmcontinue'])


def api_tagged_changes(tag, continue_key=None):
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'recentchanges',
        'rctag': tag,
        'rcprop': 'title|timestamp|ids',
        'rclimit': 'max',
        'rctype': 'edit|new|log|categorize|external'
    }

    if continue_key is not None:
        params['rccontinue'] = continue_key

    response = requests.get(
        'https://commons.wikimedia.org/w/api.php',
        params=params
    ).json()

    return (response['query']['recentchanges'],
            response['continue']['rccontinue'])


def api_info_url(pageid):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'info',
        'pageids': pageid,
        'inprop': 'url'
    }

    response = requests.get(
        'https://commons.wikimedia.org/w/api.php',
        params=params
    ).json()

    return response['query']['pages'][pageid]['fullurl']


def get_contrib_request(filter_type, filter_value, continue_key=None):
    if filter_type == 'recent':
        latest_files, continue_key = api_all_images(continue_key)

        for file in latest_files:
            file_depicts = get_file_depicts(file['title'])
            if file_depicts is not None:
                (depict_id, depict_label,
                 depict_description, claim_id) = file_depicts
            else:
                continue

            contribute_request = {
                'media_page': file['descriptionurl'],
                'media_title': file['title'],
                'depict_id': depict_id,
                'depict_label': depict_label,
                'depict_description': depict_description,
                'claim_id': claim_id,
                'csrf': gen_csrf()
            }
            return contribute_request
    elif filter_type == 'category':
        pages, continue_key = api_category_members(filter_value, continue_key)

        for page in pages:
            if page['ns'] != 6:
                continue
            file_depicts = get_file_depicts(page['title'])
            if file_depicts is not None:
                (depict_id, depict_label,
                 depict_description, claim_id) = file_depicts
            else:
                continue

            contribute_request = {
                'media_page': page['fullurl'],
                'media_page_id': page['pageid'],
                'media_title': page['title'],
                'depict_id': depict_id,
                'depict_label': depict_label,
                'depict_description': depict_description,
                'claim_id': claim_id,
                'csrf': gen_csrf()
            }
            return contribute_request
    elif filter_type == 'tag':
        changes, continue_key = api_tagged_changes(filter_value, continue_key)

        for change in changes:
            if change['ns'] != 6:
                continue
            file_depicts = get_file_depicts(change['title'])
            if file_depicts is not None:
                (depict_id, depict_label,
                 depict_description, claim_id) = file_depicts
            else:
                continue

            contribute_request = {
                'media_page': api_info_url(str(change['pageid'])),
                'media_page_id': change['pageid'],
                'media_title': change['title'],
                'depict_id': depict_id,
                'depict_label': depict_label,
                'depict_description': depict_description,
                'claim_id': claim_id,
                'csrf': gen_csrf()
            }
            return contribute_request

    return get_contrib_request(filter_type, filter_value, continue_key)


def gen_csrf():
    csrf = secrets.token_hex(16)
    session['csrf'] = csrf
    return csrf


def get_file_depicts(file_name):
    statements = requests.get(
        'https://commons.wikimedia.org/w/api.php',
        params={
            'action': 'wbgetentities',
            'format': 'json',
            'sites': 'commonswiki',
            'titles': file_name
        }
    ).json()

    try:
        statements = (list(statements['entities'].values())
                      [0]['statements'])

        if 'P180' not in statements:
            return None

        depict_id = (statements['P180'][0]['mainsnak']['datavalue']
                     ['value']['id'])
        claim_id = statements['P180'][0]['id']

        depict = requests.get(
            'https://www.wikidata.org/w/api.php',
            params={
                'action': 'wbgetentities',
                'format': 'json',
                'ids': depict_id,
                'languages': 'en'
            }
        ).json()['entities'][depict_id]
        depict_label = depict['labels']['en']['value']
        depict_description = depict['descriptions']['en']['value']

        return (depict_id, depict_label, depict_description, claim_id)
    except KeyError:
        return None
