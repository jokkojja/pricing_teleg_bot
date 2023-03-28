# import datetime
# import itertools
# import os
# import re
# import time
# from bs4 import BeautifulSoup
# import cloudscraper
# import logging
# from tqdm import tqdm
# from config import (
#     MAX_COUNT_OF_ADDS,
#     MAX_COUNT_OF_PAGE,
#     HEADERS,
#     START_URL,
#     ROOMS_MATCHING_DICT,
#     LOGS_PATH,
#     SCRAPE_LOG_PATH,
#     DATA_PATH
#     )

# class CianUrlsParser:
#     def __init__(self, rooms: str) -> None:
#         """_summary_

#         Args:
#             rooms (str): _description_
#         """
#         self.__MAX_COUNT_OF_ADDS = MAX_COUNT_OF_ADDS
#         self.__MAX_COUNT_OF_PAGE = MAX_COUNT_OF_PAGE
#         self.__MAX_COUNT_OF_PROPERTIES = self.__MAX_COUNT_OF_PAGE * self.__MAX_COUNT_OF_ADDS
#         self.keep_data_path = DATA_PATH
#         self.logs_path = LOGS_PATH
#         self.rooms_url = ROOMS_MATCHING_DICT[rooms]
#         self.scrape_log_file = SCRAPE_LOG_PATH
#         self.scrapper = cloudscraper.CloudScraper()
#         self.scrapper.headers = HEADERS
#         self.start_url = START_URL + self.rooms_url
        
#     def get_count_of_pages(self) -> int:
#         """_summary_

#         Returns:
#             int: _description_
#         """
#         page = self.scrapper.get(url = self.start_url)
#         soup = BeautifulSoup(page.text, 'html.parser')
#         text_count_page = soup.find('h5', {'class': '_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_20px--tUURJ _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6'}).text
#         count_of_adds = int(''.join(re.findall(r'\d+', text_count_page)))
#         count_of_pages = count_of_adds // 50 + 1
#         return count_of_pages

#     def get_info_about_adds(self) -> None:
#         """_summary_
#         """
#         count_of_pages = get_count_of_pages()
#         ret = f"Count of pages: {count_of_pages}, potential count of add to scrape: {__MAX_COUNT_OF_PROPERTIES}"
    
#     def write_to_file(self, values: list) -> None:
#         file_name = os.path.join(self.keep_data_path, 'rooms1_' + datetime.datetime.now().strftime("%m_%d_%Y-%H:%M:%S") + '.txt')
#         with open(file_name, 'a+') as file:
#             [file.write(value + '\n') for value in values]
#         print(f"Urls file with name {file_name} saved into {self.keep_data_path}")
        
#     def scrape(self) -> None:
#         """_summary_
#         """
#         count_of_pages = self.get_count_of_pages()
#         if count_of_pages > self.__MAX_COUNT_OF_PAGE:
#             print(f"Count of pages is more then {__MAX_COUNT_OF_PAGE}. Scrapping only {__MAX_COUNT_OF_PAGE} pages")
#             count_of_pages = self.__MAX_COUNT_OF_PAGE
            
#         print(f"Started scrapping. Count of pages: {count_of_pages}\n")
#         all_hrefs = []
#         for page in tqdm(range(1, count_of_pages + 1)):
#             url = self.start_url + f'&p={page}'
#             soup = BeautifulSoup(self.scrapper.get(url = url).text, 'html.parser')
#             objects = soup.findAll('a', {'class': '_93444fe79c--media--9P6wN'})
#             hrefs = [i.get('href') for i in objects]
#             all_hrefs.append(hrefs)
#             time.sleep(2)
#         all_hrefs = list(itertools.chain(*all_hrefs))
#         self.write_to_file(all_hrefs)
