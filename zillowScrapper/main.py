import zillow_parser as zp
import os, sys
from selenium import webdriver
import logging
import config


def main():
    """
    Set chromedriver and call methods of zillow_parse class.
    :return:
    """
    # deine chromdriver
    chromedriver = config.chromedriver_path
    # r"C:\Users\49176\OneDrive\Desktop\chromedriver_win32/chromedriver.exe"  # path to the chromedriver executable
    chromedriver = os.path.expanduser(chromedriver)
    sys.path.append(chromedriver)
    driver = webdriver.Chrome(chromedriver)
    logging.info("data parser started")
    zillow_parser = zp.ZillowData(driver, chromedriver, config.zillow_url)  # 'https://www.zillow.com/new-york-ny/'
    df = zillow_parser.get_all_data(chromedriver, driver, pages=config.pages)
    zillow_parser.stat_of_data(df)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
