from properties_parser import CianPropertyParser


if __name__ == "__main__":
    count_scrapped_pages = 0
    count_scrapped_properties = 0
    for i in range(7):
        scrapper = CianPropertyParser(i)
        scrapper.scrapping()
        scrapper.get_result()
        count_scrapped_pages += scrapper.get_count_of_pages()
        count_scrapped_properties += scrapper.get_count_scrapped_properties()
    print(f"RESULT: SCRAPPED PAGES: {count_scrapped_pages} \n\
            SCRAPPED PROPERTIES: {count_scrapped_properties}")