# Import beautifulsoup library for webscraping
from bs4 import BeautifulSoup

# Import requests library to request infomation from websites
import requests

# Import json library
import json

# import psycopg2 module to connect to PostgreSQL database
import psycopg2

# Import date class from datetime module
from datetime import date

# Define database info
hostname = 'localhost'
database = 'it_car_dealers_db'
username = 'postgres'
pwd = 'Dice123!'
port_id = '5432'

# Reset connection and cursor
conn = None
cursor = None

# Connect to database
conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

#  Configure class
class DealersInfo:
    def __init__(self, location, advert_url, profile_url, company_name, company_email_address, company_website, company_tel_1):
        self.location = location
        self.advert_url = advert_url
        self.profile_url = profile_url
        self.company_name = company_name
        self.company_email_address = company_email_address
        self.company_website = company_website
        self.company_tel_1 = company_tel_1

# Configure headers to send fake user agent with every request. This fixes 403 response when making a response
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# Set import date as the current day
import_date = date.today()

number_of_pages = 1000

# Print messsage in terminal to know that scraping is in progress
print(f'Scaping Subito in progress...')

counter = 0 

for i in range(1, number_of_pages):

    i = str(i)

    # The main page to scrape from
    main_site = 'https://www.subito.it/annunci-sardegna/vendita/auto/?o=' + i + '&advt=1%2C2'

    # Get information from bakeca.it
    webpage_1 = requests.get(main_site, headers=HEADERS).text
    
    # # Create instance of beautifulsoup for webpage_1
    soup = BeautifulSoup(webpage_1, 'lxml')

    # Get advert listing elements
    advert_containers = soup.findAll('div', class_='items__item item-card item-card--big BigCard-module_card__Exzqv',)

    for advert_container in advert_containers:
        try:
            # Get location
            dealer_location = advert_container.find('span', class_='index-module_sbt-text-atom__ed5J9 index-module_token-caption__TaQWv index-module_size-small__XFVFl index-module_weight-semibold__MWtJJ index-module_town__2H3jy').text

            # Advert url
            advert_url = advert_container.find('a', class_='BigCard-module_link__kVqPE').get('href')

            # Get information from webpage 2
            webpage_2 = requests.get(advert_url, headers=HEADERS,).text

            # Create instance of beautifulsoup for webpage_2
            soup = BeautifulSoup(webpage_2, 'lxml')

        except AttributeError:
            dealer_location = None
            advert_url = None


        try:
            # Get dealer profile url
            dealer_profile_url = soup.find('a', class_='UserDetails_shop-details-wrapper__52W3J UserDetails_shop-link__vtEs8').get('href')

            # Get information from webpage 3
            webpage_3 = requests.get(dealer_profile_url, headers=HEADERS,).text

            # Create instance of beautifulsoup for webpage_2
            soup = BeautifulSoup(webpage_3, 'lxml')

            # Get company name
            dealer_name = soup.find('div', class_='shop_main_info_row').find('h1').text
            dealer_name = dealer_name.title()

            # Set email address to None
            dealer_email_address = None

        except AttributeError:
            dealer_profile_url = None
            dealer_name = None

        try:
            # Get company website
            dealer_website = soup.find('a', class_='shop_site_link').get('href')

            # Get telephone number
            dealer_tel_number_1 = soup.find('div', class_='phone_row').find('span').text

        except AttributeError:
            dealer_website = None
            dealer_tel_number_1 = None

        
        # Open a cursor to perform SQL operationa
        cursor = conn.cursor()

        # Insert data into table
        insert_script = 'INSERT INTO subito_raw (company_name, company_website, company_email_address, company_tel, profile_url, location, advert_url, import_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        insert_values = (dealer_name, dealer_website, dealer_email_address, dealer_tel_number_1, dealer_profile_url, dealer_location, advert_url, import_date)

        # Execute insert script to insert values into the table
        cursor.execute(insert_script, insert_values)

        # Commit execution
        conn.commit()

        # Populate object with dealers info
        # dealers_info = DealersInfo(dealer_location, advert_url, dealer_profile_url, dealer_name, dealer_email_address, dealer_website, dealer_tel_number_1)

        # Convert python object to json object
        # dealers_info_json = json.dumps(dealers_info.__dict__)

        # Print each object in the terminal
        # print(dealers_info_json)

        counter = counter + 1

        print(f'Records added to database: {counter}')

        if advert_container == None:
            break

print(f'Scaping {main_site} - COMPLETE')

conn.close()