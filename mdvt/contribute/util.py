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


def get_contrib_request(continue_key=None):
    latest_files, continue_key = api_allimages(continue_key)

    for file in latest_files:
        statements = requests.get(
            'https://commons.wikimedia.org/w/api.php',
            params={
                'action': 'wbgetentities',
                'format': 'json',
                'sites': 'commonswiki',
                'titles': file['title']
            }
        ).json()

        try:
            statements = (list(statements['entities'].values())
                          [0]['statements'])
        except KeyError:
            continue

        if 'P180' not in statements:
            continue

        depict_id = (statements['P180'][0]['mainsnak']['datavalue']
                     ['value']['id'])

        try:
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
        except KeyError:
            continue

        contribute_request = {
            'media': file['title'],
            'depict_id': depict_id,
            'depict_label': depict_label,
            'depict_description': depict_description
        }
        return contribute_request

    get_contrib_request(continue_key)
