from properties_parser import CianPropertyParser


if __name__ == "__main__":
    for i in range(7):
        scrapper = CianPropertyParser(i)
        scrapper.scrapping()
        scrapper.print_result()