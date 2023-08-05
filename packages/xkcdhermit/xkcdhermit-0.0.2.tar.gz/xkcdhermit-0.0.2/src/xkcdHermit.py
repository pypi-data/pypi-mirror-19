r"""
      _           _   _   _                     _ _   
     | |         | | | | | |                   (_) |  
__  _| | _____ __| | | |_| | ___ _ __ _ __ ___  _| |_ 
\ \/ / |/ / __/ _` | |  _  |/ _ \ '__| '_ ` _ \| | __|
 >  <|   < (_| (_| | | | | |  __/ |  | | | | | | | |_ 
/_/\_\_|\_\___\__,_| \_| |_/\___|_|  |_| |_| |_|_|\__|
                                                      
                                                      
There exists an xkcd comic for everything. 
xkcdHermit aims to respond to everything using an appropriate comic.
 
""" 

import os
import itertools
from operator import itemgetter
import requests
import pprint

try:
    from . import log  # entry_point case

except:
    import log  # __main__ case



NLP_ENDPOINT = "https://api.textrazor.com"

try:
	NLP_KEY = os.environ['textrazor_key']

except KeyError:
    log.log_error("Error: Couldn't find textrazor key")
    exit()


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

    for entity in entities:
        print(output_format.format(entity['confidenceScore'], entity[
              'entityId'], entity['wikiLink']))

    '''
    getvals = itemgetter('entityId')

    for _, groups in itertools.groupby(entities, getvals):
        result.append(next(groups))

    for entity in result:
        print(output_format.format(entity['confidenceScore'], entity[
              'entityId'], entity['wikiLink']))
    '''


def main():

    query = "Angry passengers create turbulence for the airlines."
    _nlp_response(query)




if __name__ == '__main__':
    main()
