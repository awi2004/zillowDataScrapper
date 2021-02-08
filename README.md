# zillowScrapper
zillowScraper: It scrapes the data from zillow website and does the following:

1. Scrape the data from Zillow (for ex: New York listings) 
    
    https://www.zillow.com/new-york-ny/

2. Go through all the listings there
3. Collect all the data points from the listing:



        a. Link
        b. How many days on Zillow and views
        c. Price of the listing : for ex $399.000
        d. How many bedrooms
        e. How many bathrooms
        f. Size of apartmemt in Square meters/feets
        g. Type of the ad
        h. Address and city of the apartment
        i. Company/Broker
4. Show stats on the collected data:


        a. How many properties
        b. Average price (in total) and per sq.ft.
        c. Number of properties per type of the ad
        d. Number of properties per company/brok
    
    
    
zillowScrapper has below Python files:

    1. zillow_parser.py: it contains all the logic for scraper.
    2. main.py: it has a main method to run the methods of zillow_parser.
    3. config.py: it contains below user defined variables
            chromdriver_path : path to chromedriver
            url: link of zillow website to scrape data for ex Neyowrk listings  https://www.zillow.com/new-york-ny/ 
            pages: number of pages for the listings.

Steps to run zillowScrapper:


    a. Install necessary Python packages:
            pip install -r requirements.txt
    b. Run main.py
