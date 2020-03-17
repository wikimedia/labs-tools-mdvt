import requests


def api_allimages(continue_key=None):
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


def api_categorymembers(category_name, continue_key=None):
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


def get_contrib_request(filter_type, filter_value, continue_key=None):
    if filter_type == 'recent':
        latest_files, continue_key = api_allimages(continue_key)

        for file in latest_files:
            file_depicts = get_file_depicts(file['title'])
            if file_depicts is not None:
                depict_id, depict_label, depict_description = file_depicts
            else:
                continue

            contribute_request = {
                'media_page': file['descriptionurl'],
                'media_title': file['title'],
                'depict_id': depict_id,
                'depict_label': depict_label,
                'depict_description': depict_description
            }
            return contribute_request
    elif filter_type == 'category':
        pages, continue_key = api_categorymembers(filter_value,
                                                  continue_key)

        for page in pages:
            if page['ns'] != 6:
                continue
            file_depicts = get_file_depicts(page['title'])
            if file_depicts is not None:
                depict_id, depict_label, depict_description = file_depicts
            else:
                continue

            contribute_request = {
                'media_page': page['fullurl'],
                'media_title': page['title'],
                'depict_id': depict_id,
                'depict_label': depict_label,
                'depict_description': depict_description
            }
            return contribute_request

    return get_contrib_request(filter_type, filter_value, continue_key)


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

        return (depict_id, depict_label, depict_description)
    except KeyError:
        return None
