import os
from bs4 import BeautifulSoup
import logging
import time
import sys
import numpy as np
import pandas as pd
import pickle


class ZillowData:
    """
    Zillow data scrapper.
    """

    def __init__(self, driver, chromedriver, url):
        """
        Contructor
        """
        self.driver = driver
        self.chromedriver = chromedriver
        self.url = url

    def get_house_links(self, url, driver, pages=20):
        """
        Function to fetch list of house links on all the defined pages.
        :param url: link of the page.
        :param driver: selenium driver instance.
        :param pages: how many pages to scrape the listing.
        :return: list of house links on all the defined pages.
        """
        # list to store links of houses on desired pages
        house_links = []
        try:
            for i in range(0, pages):
                # set url for each page by appending _p/ to base_url
                # for exaple to navigate to page 2: url+'2'+'_p/' i.e https://www.zillow.com/new-york-ny/2_p
                self.url = self.url + str(i + 1) + '_p/'

                # navigate to page
                self.driver.get(url)
                # sleep for N secs
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # get the tags for listings
                listings = soup.find_all("a", class_="list-card-link list-card-link-top-margin list-card-img")

                # get href or link from listings
                page_data = [row['href'] for row in listings]
                print("listing of houses on page  " + str(i + 1) + " is " + str(len(page_data)))

                # store page links into the list
                house_links.append(page_data)
                time.sleep(4)

            return [j for i in house_links for j in i]  # flatten and resturn the house links as list.
        except:
            return 'None'

    def get_html_data(self, base_url):
        """
        Function to  extract html data of the page using BeautifulSoup
        :param base_url: link of the particular house on the page listings.
        :return: extracted data of html page with all tags.
        """
        try:
            # navigate to page
            self.driver.get(base_url)
            time.sleep(3)
            # extract html data of the page using BeautifulSoup
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # driver.close()
            return self.soup
        except:
            return 'None'

    def get_num_beds(self, soup):
        """
        Function to get number of bed, bathroom and size of apartment in sqfeet.
        :param soup: extracted html data of a  page with all tags.
        :return: umber of bed, bathroom and size of apartment in sqfeet.
        """
        try:
            # extract data of the page which holds information about the beds, bathroom,flat size.
            html_data = self.soup.find_all("span", class_='ds-bed-bath-living-area')
            # extract bed info
            bedroom = html_data[0].text.split()[0]
            # extract bathroom info
            bathroom = html_data[1].text.split()[0]
            # extract apartment size
            size = html_data[2].text.split()[0]
            return bedroom, bathroom, size
        except:
            return 'None', 'None', 'None'

    def get_addresss(self, soup):
        """
        Function to get address of the listing.
        :param soup: extracted html data of a  page with all tags.
        :return: address and city of the apartment.
        """
        try:
            # extract data of the page which holds information about the address.
            html_data = self.soup.find_all("h1",
                                           class_='Text-c11n-8-18-0__aiai24-0 StyledHeading-c11n-8-18-0__ktujwe-0 efSAZl')
            # extract address of the apartment
            address = html_data[0].text.split(',')[0] + ' ' + html_data[0].text.split(',')[1].rsplit('\xa0')[1] \
                      + html_data[0].text.split(',')[2]
            # extract city of the apartment
            city = html_data[0].text.split(',')[1].rsplit('\xa0')[1]
            return address, city
        except:
            return 'None', 'None'

    def get_ad_days_views(self, soup):
        """
        Function to get number of days and views for the ad
        :param soup: extracted html data of a  page with all tags.
        :return: number of days and views for the ad
        """
        try:
            # extract data of the page which holds information how long ad listed on Zillow page.
            html_data = self.soup.find_all("div", class_='Text-c11n-8-18-0__aiai24-0 einFCw')
            # extract number of days of ad
            zillow_days = html_data[0].text.split()[0]
            # extract number of views for the ad
            views = html_data[1].text.split()[0]
            return zillow_days, views
        except:
            return 'None', 'None'

    def get_price(self, soup):
        """
        Function to get price of the apartment
        :param soup: extracted html data of a  page with all tags.
        :return: price of the apartment
        """
        try:
            # extract data of the page which holds information apartment price.
            html_data = self.soup.find_all("h4",
                                           class_='Text-c11n-8-18-0__aiai24-0 StyledHeading-c11n-8-18-0__ktujwe-0 gcaUyc sc-pHIBf jLwdeZ')
            # extract price of the apartment
            price = html_data[0].text.split()[0].rsplit('$')[1]
            return price
        except:
            return 'None'

    def get_type_of_ad(self, soup):
        """
        Function to get ad type.
        :param soup: extracted html data of a  page with all tags.
        :return: ad type.
        """
        try:
            # extract data of the page which holds information type of ad.
            html_data = self.soup.find_all("span", class_='sc-pYA-dN ivRwcz ds-status-details')
            # extract ad type.
            ad_type = html_data[0].text
            return ad_type
        except:
            return 'None'

    def get_company(self, soup):
        """
        Function to get company or broker who listed the ad.
        :param soup: extracted html data of a  page with all tags.
        :return: company or broker who listed the ad.
        """
        try:
            # extract data of the page which holds information company/broker listed the ad.
            html_data = soup.find_all("strong", class_='Text-c11n-8-18-0__aiai24-0 dokllX')
            # extract commpany or broker info
            company = html_data[0].text
            return company
        except:
            return 'None'

    def get_agent(self, soup):
        """
        Function to get agent or owner  who listed the ad.
        :param soup: extracted html data of a  page with all tags.
        :return: agent or owner  who listed the ad.
        """
        try:
            # extract data of the page which holds information agent or owner who listed the ad.
            html_data = self.soup.find_all("p", class_='Text-c11n-8-18-0__aiai24-0 foiYRz')
            # extract agent or owner info
            agent = html_data[0].text
            return agent
        except:
            return 'None'

    def get_zillow_data(self, soup, link):
        """
        Function to get all the features of a house.
        :param soup: extracted html data of a  page with all tags.
        :param link: link of the house from which we extract data.
        :return: list containing all the features of a house.
        """

        # store all the
        zillow_house_data = []
        bedroom, bathroom, size = self.get_num_beds(self.soup)
        address, city = self.get_addresss(self.soup)
        zillow_days, views = self.get_ad_days_views(self.soup)
        price = self.get_price(self.soup)
        ad_type = self.get_type_of_ad(self.soup)
        company = self.get_company(self.soup)
        agent = self.get_agent(self.soup)

        zillow_house_data.append(
            [bedroom, bathroom, size, address, city, zillow_days, views, price, ad_type, company, agent, link])
        return zillow_house_data

    def get_all_data(self, chromedriver, driver, pages=20):
        """
        :param chromedriver: chrome drive path to run url and extract data.
        :param driver: driver instance to use selenium.
        :param pages: number of pages to scrape.
        :return: pandas dataframe containing houses  information.
        """
        print('chromedriver path: {}'.format(self.chromedriver))
        sys.path.append(self.chromedriver)
        # self.driver = webdriver.Chrome(self.chromedriver)
        houses = self.get_house_links(self.url, self.driver, pages)
        print("------calculations house links done--------")
        zillow_data = []
        for i in range(0, len(houses)):
            # driver = webdriver.Chrome(chromedriver)
            soup = self.get_html_data(houses[i])
            # time.sleep(3)
            zillow_data.append(self.get_zillow_data(soup, houses[i]))
            time.sleep(4)

        with open('zillow_data.pkl', 'wb') as f:
            pickle.dump(zillow_data, f)
        df = pd.DataFrame([j for i in zillow_data for j in i])
        columns = ['bedroom', 'bathroom', 'size', 'address', 'city', 'zillow_days', 'views', 'price', 'ad_type',
                   'company', 'agent', 'link']
        df.columns = columns
        df.to_csv('zillow_data.csv', index=False)
        print("-----dataframe crated ------")
        self.driver.close()
        return df

    def stat_of_data(self, df):
        """
        Function to print statics about the scraped data
        :param df: dataframe which holds all the scraped data
        :return: nothing.
        """
        print('Number of unique properties per  page {}'.format(40))
        print('Number of unique properties on all  pages {}'.format(df['link'].nunique()))
        print('Number of properties per type of the ad   ')
        print(df.ad_type.value_counts())
        print('        ')

        print('Number of properties per company/broker  ')
        print(df.agent.value_counts())

        df['price'] = df['price'].apply(lambda x: x.replace(',', ''))
        df['size'] = df['size'].apply(lambda x: x.replace(',', '') if x != 'None' else '0')
        df['size'] = df['size'].apply(lambda x: x.replace(',', '') if x != '--' else '0')
        print('Average price (in total): ${} '.format(np.average(df['price'].astype(int))))
        print('Average price per sq.ft: ${} '.format(
            round((np.average(df['price'].astype(int)) / np.average(df['size'].astype(int))), 4)))
        results = {'Number of unique properties per  page ': 40,
                   'Number of properties per page ': df['link'].nunique(),
                   'Number of properties per type of the ad   ': df.ad_type.value_counts(),
                   'Number of properties per company/broker  ': df.agent.value_counts(),
                   'Average price (in total)$: ': np.average(df['price'].astype(int)),
                   'Average price per sq.ft$: ': round(
                       (np.average(df['price'].astype(int)) / np.average(df['size'].astype(int))), 4)}
        print(type(results))
        with open('results.txt', 'w') as file:
            file.write(str(results))
        return results
