import requests
from bs4 import BeautifulSoup
import bs4
import logging
from dataclasses import dataclass, field, asdict
import re
import cloudscraper
import time
import os
from tqdm import tqdm
import tqdm
import datetime
import itertools
import json
import ast
from config import (
    MAX_COUNT_OF_ADDS,
    MAX_COUNT_OF_PAGE,
    HEADERS,
    START_URL,
    ROOMS_MATCHING_DICT,
    LOGS_PATH,
    SCRAPE_LOG_PATH,
    DATA_PATH,
    API_JSON,
    API_ADDRESS
    )


@dataclass
class Property:
    "Dataclass for keeping proeprty attributes"
    coordinates: str = field(default=None)
    description: str = field(default=None)
    url: str = field(default=None)
    offer_id: str = field(default=None)
    date: str = field(default=None)
    price: str = field(default=None)
    address: str = field(default=None)
    area: str = field(default=None)
    rooms: str = field(default=None)
    floor: str = field(default=None)
    total_floor: str = field(default=None)
    images: str = field(default=None)


class PropertyParser:
    def __init__(self, rooms: str):
        self.__MAX_COUNT_OF_ADDS = MAX_COUNT_OF_ADDS
        self.__MAX_COUNT_OF_PAGE = MAX_COUNT_OF_PAGE
        self.__MAX_COUNT_OF_PROPERTIES = self.__MAX_COUNT_OF_PAGE * self.__MAX_COUNT_OF_ADDS
        self.keep_data_path = DATA_PATH
        self.logs_path = LOGS_PATH
        self.room = room
        self.rooms_url = ROOMS_MATCHING_DICT[self.room]
        self.scrape_log_file = SCRAPE_LOG_PATH
        self.scrapper = cloudscraper.CloudScraper()
        self.scrapper.headers = HEADERS
        self.scrapper.url = API_ADDRESS
        self.json_params = API_JSON  
        self.start_url = START_URL + self.rooms_url
        self.offers = []
        
    def set_room_in_api(self):
        self.json_params['jsonQuery']['room']['value'].append(int(self.room))
    
    def set_page_in_api(self, page):
        self.json_params['jsonQuery']['page']['value'] = page
        
    def set_property_data(self, property):
        property_item = Property()
        property_item.coordinates = item['geo']['coordinates']
        property_item.description = item['description']
        property_item.url = item["fullUrl"]
        property_item.offer_id = item["id"]
        timestamp = datetime.datetime.fromtimestamp(item["addedTimestamp"])
        timestamp = datetime.datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
        property_item.date = timestamp
        property_item.price = item["bargainTerms"]["priceRur"]
        property_item.address = item["geo"]["userInput"]
        property_item.area = item["totalArea"]
        property_item.rooms = item["roomsCount"]
        property_item.floor = item["floorNumber"]
        property_item.total_floor = item["building"]["floorsCount"]
        property_item.images = [i['fullUrl'] for i in item['photos']]
        return asdict(property_item)
    
    def get_all_offers(self, response):
        for item in data["data"]["offersSerialized"]:
            offer = get_offer(item)
            self.offers.append(offer)
    
    def get_json_from_cian(self):
        self.set_room_in_api()
        count_of_pages = self.get_count_of_pages()
        
        for page in tqdm(range(1, count_of_pages + 1)):
            self.set_page_in_api(page)
            response = self.scrapper.post(json=self.json_params).json()
            self.get_all_offers(response)
            time.sleep(2)
        
    def get_count_of_pages(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        page = self.scrapper.get(url = self.start_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        text_count_page = soup.find('h5', {'class': '_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_20px--tUURJ _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6'}).text
        count_of_adds = int(''.join(re.findall(r'\d+', text_count_page)))
        count_of_pages = count_of_adds // 50 + 1
        if count_of_pages > self.__MAX_COUNT_OF_PAGE:
            count_of_pages = self.__MAX_COUNT_OF_PAGE
        return count_of_pages
    
    def write_properties_json(self):
        json_data = json.dumps({'properties': self.offers})
        file_name = os.path.join(self.keep_data_path, f'rooms_{self.room}' + datetime.datetime.now().strftime("%m_%d_%Y-%H:%M:%S") + '.json')
        with open(file_name, 'w+') as file:
            file.write(json_data)
    
    def scrapping(self):
        # add main functionality
        pass
        

