from dataclasses import dataclass, field, asdict
import datetime
import json
import os
import re
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import cloudscraper
import logging
from config import (
    API_ADDRESS,
    API_JSON,
    COUNT_PAGE_CLASS,
    DATA_PATH,
    HEADERS,
    LOGS_PATH,
    MAX_COUNT_OF_PAGE,
    ROOMS_MATCHING_DICT,
    SCRAPE_LOG_PATH,
    START_URL,
    )
#TODO: Add logging (info, errors, problems)

@dataclass
class Property:
    " Dataclass for keeping property attributes"
    coordinates: dict = field(default=None)
    description: str = field(default=None)
    url: str = field(default=None)
    offer_id: int = field(default=None)
    date: str = field(default=None)
    price: int = field(default=None) #RUB
    address: str = field(default=None)
    area: float = field(default=None)
    rooms: int = field(default=None)
    floor: int = field(default=None)
    images: list = field(default=None)
    buildingBuildYear: int = field(default=None)
    buildingParkingType: str = field(default=None)
    buildingMaterialType: str = field(default=None)
    buildingFloorsCount: int = field(default=None)
    layout: str = field(default=None)
    offerType: str = field(default=None)
    dealType: str = field(default=None)
    isApartments: str = field(default=None)
    kitchenArea: float = field(default=None)
    balconiesCount: int = field(default=None)
    isBuildingCommissioned: str = field(default=None)


class CianPropertyParser:
    """ Cian parser class
    """
    def __init__(self, room: int) -> None:
        """ Initialize parser object.

        Args:
            rooms (int): Room params for creating json for API request.
            Possible values: 0 (it means studio), 1, 2, 3, 4, 5, 6
        """
        assert isinstance(room, int), "room argument shoud be int" 
        assert room in [0, 1, 2, 3, 4, 5, 6] , "Ivalid room value. Possible values: 0, 1, 2, 3, 4, 5, 6"
        self.__max_count_of_page = MAX_COUNT_OF_PAGE
        self.__count_scrapped_pages = 0
        self.__count_scrapped_properties = 0     
        self.keep_data_path = DATA_PATH
        self.logs_path = LOGS_PATH
        self.room = room
        self.rooms_url = ROOMS_MATCHING_DICT[str(self.room)]
        self.scrape_log_file = SCRAPE_LOG_PATH
        self.scrapper = cloudscraper.CloudScraper()
        self.scrapper.headers = HEADERS
        self.scrapper.url = API_ADDRESS
        self.json_params = API_JSON
        self.start_url = START_URL + self.rooms_url
        self.offers = []
        
    def set_room_in_api(self) -> None:
        """ Set room in json for API request
        """
        self.json_params['jsonQuery']['room']['value'].append(self.room)
    
    def set_page_in_api(self, page: int):
        """ Set page in json for API request

        Args:
            page (int): Number of page
        """
        self.json_params['jsonQuery']['page']['value'] = page
        
    def prepare_property_data(self, property_data: dict) -> dict:
        """ Prepare Property object with extracted attributes

        Args:
            property_data (dict): All data about single property

        Returns:
            dict: extracted siingle property attributes
        """
        property_item = Property()
        property_item.coordinates = property_data['geo']['coordinates']
        property_item.description = property_data['description']
        property_item.url = property_data["fullUrl"]
        property_item.offer_id = property_data["id"]
        timestamp = datetime.datetime.fromtimestamp(property_data["addedTimestamp"])
        timestamp = datetime.datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
        property_item.date = timestamp
        property_item.price = property_data["bargainTerms"]["priceRur"]
        property_item.address = property_data["geo"]["userInput"]
        try:
            property_item.area = float(property_data["totalArea"])
        except TypeError:
            pass # if none field
        property_item.rooms = property_data["roomsCount"]
        property_item.floor = property_data["floorNumber"]
        property_item.images = [i['fullUrl'] for i in property_data['photos']]
        property_item.buildingBuildYear = property_data['building']['buildYear']
        try:
            property_item.buildingParkingType = property_data['building']['parking']['type']
        except TypeError:
            pass # if none field
        property_item.buildingMaterialType = property_data['building']['materialType']
        property_item.buildingFloorsCount = property_data['building']['floorsCount']
        property_item.layout = property_data['layout']
        property_item.offerType = property_data['offerType']
        property_item.dealType = property_data['dealType']
        property_item.isApartments = property_data['isApartments']
        try:
            property_item.kitchenArea = float(property_data['kitchenArea'])
        except TypeError:
            pass # if none field
        property_item.balconiesCount = property_data['balconiesCount']
        try:
            property_item.isBuildingCommissioned = property_data['factoids'][0]['text']
        except IndexError:
            pass # if none field
        return asdict(property_item)
    
    def get_all_offers(self, json_response: dict) -> None:
        """ Preparing all properties loop

        Args:
            json_response (dict): single dict with data about property
        """
        for item in json_response["data"]["offersSerialized"]:
            offer = self.prepare_property_data(item)
            self.offers.append(offer)
            self.__count_scrapped_properties += 1
    
    def scrapping(self) -> None:
        """ Main scrapping loop
        """
        print(f"\nStarted scrapping properties with {self.room} rooms.. \n")
        self.set_room_in_api()
        count_of_pages = self.get_count_of_pages()
        for page in tqdm(range(1, count_of_pages + 1)):
            self.set_page_in_api(page)
            json_response = self.scrapper.post(url=API_ADDRESS, json=self.json_params).json()
            self.get_all_offers(json_response)
            self.__count_scrapped_pages += 1
            time.sleep(5)
        self.write_properties_json()
        
    def get_count_of_pages(self) -> int:
        """ Get count of pages are possible for scrapping

        Returns:
            int: Count of pages
        """
        page = self.scrapper.get(url = self.start_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        text_count_page = soup.find('h5', {'class': COUNT_PAGE_CLASS}).text
        count_of_adds = int(''.join(re.findall(r'\d+', text_count_page)))
        count_of_pages = count_of_adds // 50 + 1
        if count_of_pages > self.__max_count_of_page:
            count_of_pages = self.__max_count_of_page
        return count_of_pages
    
    def write_properties_json(self) -> str:
        """ Write all scrapped properties into json

        Returns:
            str: Filename in which data were saved
        """
        json_data = json.dumps({'properties': self.offers})
        file_name = os.path.join(
            self.keep_data_path,
            f'rooms{self.room}-' + 
            datetime.datetime.now().strftime("%m_%d_%Y-%H:%M:%S") +
            '.json'
            )
        with open(file_name, 'w+', encoding='utf-8') as file:
            file.write(json_data)
        return file_name
    
    def print_result(self) -> None:
        """Generating message with info about count of processed pages
           and prepared properties
        """
        message = f"During scrapping {self.room} rooms \
                    {self.__count_scrapped_pages} pages were processed \
                    and {self.__count_scrapped_properties} properties were saved."
        print(message)
if __name__ == "__main__":
    for i in range(7):
        scrapper = CianPropertyParser(i)
        scrapper.scrapping()
        scrapper.get_result()
