import os
#requests params
MAX_COUNT_OF_PAGE = 54
MAX_COUNT_OF_ADDS = 28
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML,[] like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
START_URL = 'https://kemerovo.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4795&'
API_JSON = {
    'jsonQuery': {
        '_type': 'flatsale',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                4795,
            ],
        },
        'room': {
            'type': 'terms',
            'value': [
                #append rooms (1,2,3 and etc)
            ],
        },
        'page': {
            'type': 'term',
            'value': 2, # use pagination
        },
    },
}
API_ADDRESS = 'https://api.cian.ru/search-offers/v2/search-offers-desktop/'

#mathcing
ROOMS_MATCHING_DICT = {'1': 'room1=1',
'2': 'room2=1',
'3': 'room3=1',
'4': 'room4=1',
'5': 'room5=1',
'6': 'room6=1',
'studio': 'room9=1'}

#paths
LOGS_PATH = 'logs'
SCRAPE_LOG_PATH = os.path.join(LOGS_PATH, 'cian_scrapper.txt') 
DATA_PATH = 'data'