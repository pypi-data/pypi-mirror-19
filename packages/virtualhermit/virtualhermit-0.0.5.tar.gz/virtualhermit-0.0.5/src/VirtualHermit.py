"""
 __      ___      _               _   _    _                     _ _   
 \ \    / (_)    | |             | | | |  | |                   (_) |  
  \ \  / / _ _ __| |_ _   _  __ _| | | |__| | ___ _ __ _ __ ___  _| |_ 
   \ \/ / | | '__| __| | | |/ _` | | |  __  |/ _ \ '__| '_ ` _ \| | __|
    \  /  | | |  | |_| |_| | (_| | | | |  | |  __/ |  | | | | | | | |_ 
     \/   |_|_|   \__|\__,_|\__,_|_| |_|  |_|\___|_|  |_| |_| |_|_|\__|
                                                                       

Virtual Hermit checks your social media newsfeed before you waste time on it.

""" 
import os
import itertools
from operator import itemgetter
import requests

os.chdir(os.path.dirname(__file__))

from log import log_error



NLP_ENDPOINT = "https://api.textrazor.com"
FB_ENDPOINT = "graph.facebook.com"

try:
	NLP_KEY = os.environ['textrazor_key']

except KeyError:
    log_error("Error: Couldn't find textrazor key")
    exit()


FB_KEY = ""


def _nlp_response(message):

    output_format = " Score : {} \n Topic : {} \n Wiki : {} \n"

    header = {
        'X-TextRazor-Key': NLP_KEY,
        'Accept-encoding': 'gzip',
        'cleanup.return': 'true',
    }

    data = {
        'text': message,
        'cleanup.mode': 'raw',
        'extractors': ('topics', 'entities', 'categories', 'senses'),
    }

    response = requests.post(NLP_ENDPOINT, headers=header, data=data)
    response_data = response.json()

    result = entities = []

    if response.status_code == 200 and response_data['ok']:
        for entity in response_data['response']['entities']:
            if entity['confidenceScore']:
                entities.append(entity)

    entities = sorted(entities, key=itemgetter(
        'confidenceScore'), reverse=True)
    getvals = itemgetter('entityId')

    for _, groups in itertools.groupby(entities, getvals):
        result.append(next(groups))

    for entity in result:
        print(output_format.format(entity['confidenceScore'], entity[
              'entityId'], entity['wikiLink']))


def main():
    query = "I chose to go to MIT over Stanford for grad school."
    _nlp_response(query)

if __name__ == '__main__':
    main()
