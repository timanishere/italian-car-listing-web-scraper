# Import json library
import json

# Import beautifulsoup library for webscraping
from bs4 import BeautifulSoup

# Import requests library to request infomation from websites
import requests

# import psycopg2 module to connect to PostgreSQL database
import psycopg2

# Import to encode strings
from unidecode import unidecode

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

# The main page to scrape from
main_site = 'https://www.autoscout24.it/lst?atype=C&cy=I&damaged_listing=exclude&desc=0&lat=39.30531&lon=9.20454&page=1&powertype=kw&search_id=ad0dgnwsfq&sort=standard&source=listpage_pagination&ustate=N%2CU&zip=sinnai'

# Print messsage in terminal to know that scraping is in progress
print(f'Scraping {main_site} in progress...')

# Set import date as the current day
import_date = date.today()

# Get information from bakeca.it
webpage_1 = requests.get(main_site, headers=HEADERS,).text

# Create instance of beautifulsoup for webpage_1
soup = BeautifulSoup(webpage_1, 'lxml')

# Get paginator
number_of_pages_element_arr = soup.findAll('button', class_='FilteredListPagination_button__41hHM')

# Get the last number of the page
last_page_raw = number_of_pages_element_arr[2]

last_page_raw = str(last_page_raw)

# Clean string to get number
last_page = last_page_raw.split('>')
last_page = last_page[1]
last_page = last_page.replace('</button', '')
last_page = int(last_page)

counter = 0 

for i in range(1, last_page):

    i = str(i)

    # The main page to scrape from
    main_site_loop = 'https://www.autoscout24.it/lst?atype=C&cy=I&damaged_listing=exclude&desc=0&lat=39.30531&lon=9.20454&page=' + i + '&powertype=kw&search_id=ad0dgnwsfq&sort=standard&source=listpage_pagination&ustate=N%2CU&zip=sinnai'

    # Get information from bakeca.it
    webpage_loop = requests.get(main_site_loop, headers=HEADERS,).text

    # Create instance of beautifulsoup for webpage_loop
    soup = BeautifulSoup(webpage_loop, 'lxml')
    
    # Get advert listing elements
    advert_containers = soup.findAll('article', class_='cldt-summary-full-item listing-impressions-tracking list-page-item false ListItem_article__ppamD')

    for advert_container in advert_containers:
        
        # advert url
        a_element_advert_url = advert_container.find('a', class_='ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l')

        # Convert object to string
        a_element_advert_url_str = str(a_element_advert_url)

        # Convert string to array
        a_element_advert_url_arr = a_element_advert_url_str.split(' ')

        # Get raw advert url
        advert_url_raw = a_element_advert_url_arr[4]

        # Clean raw data to get URL
        advert_url = advert_url_raw.split('">')
        advert_url = advert_url[0]
        advert_url = advert_url.replace('href="', '')
        advert_url = 'https://www.autoscout24.it/' + advert_url

        # Get information from advert page
        webpage_2 = requests.get(advert_url, headers=HEADERS,).text

        # Create instance of beautifulsoup for webpage_2
        soup = BeautifulSoup(webpage_2, 'lxml')

        
        try:
            # Get dealers location
            dealer_location = soup.find('a', class_='scr-link LocationWithPin_locationItem__pHhCa').text
            dealer_location = dealer_location.split(',')
            dealer_location = dealer_location[0]
            dealer_location = dealer_location.title()
            dealer_location = unidecode(dealer_location)

            # Get name of dealer
            dealer_name = soup.find('div', 'CommonComponents_nameContainer__3Z_zp').text
            dealer_name = dealer_name.title()

            # Get dealers profile url
            a_element_dealer_profile_url = soup.find('a', class_='scr-link DealerLinks_bold__coH8c')

            # Convert object to string
            a_element_dealer_profile_url_str = str(a_element_dealer_profile_url)

            # Convert string to array
            a_element_dealer_profile_url_arr = a_element_dealer_profile_url_str.split(' ')

            # Get raw dealer profile url
            dealer_profile_url_raw = a_element_dealer_profile_url_arr[3]

            # Clean raw data to get URL
            dealer_profile_url = dealer_profile_url_raw.replace('href="', '')
            dealer_profile_url = dealer_profile_url.replace('"', '')

            # Get information from dealer profile page
            webpage_3 = requests.get(dealer_profile_url, headers=HEADERS,).text

            # Create instance of beautifulsoup for webpage_3
            soup = BeautifulSoup(webpage_3, 'lxml')

            # Get dealer email address
            a_element_dealer_email_address = soup.find('a', class_='dp-contact-block__email')

            # Convert object to string
            dealer_email_address_str = str(a_element_dealer_email_address)

            # Convert string to array
            dealer_email_address_arr = dealer_email_address_str.split(' ')

            try:
                # Get raw dealer email address
                dealer_email_address_raw = dealer_email_address_arr[3]
            except IndexError:
                dealer_email_address_raw = None
            
            # Clean raw data to get email address
            dealer_email_address = dealer_email_address_raw.replace('href="mailto:', '')
            dealer_email_address = dealer_email_address.replace('"', '')

            # Get company website container
            div_element_dealer_website = soup.find('div', class_='dp-contact-data__container dp-contact-data__address')

            # Get <a> elements in the container
            a_elements_dealer_website_arr = div_element_dealer_website.findAll('a')

            # Get dealer website
            dealer_website_raw = a_elements_dealer_website_arr[-1]

            # Convert to string
            dealer_website_str = str(dealer_website_raw)

            # Convert string to array
            dealer_website_arr = dealer_website_str.split(' ')

            # Get raw dealer website
            dealer_website_arr_raw = dealer_website_arr[2]

            # Clean raw data to get website
            dealer_website = dealer_website_arr_raw.replace('href="', '')
            dealer_website = dealer_website.replace('"', '')

            div_element_dealer_tel_number_container = soup.find('div', class_='dp-contact-block__data')

            # Get phone number element in the container
            div_element_dealer_tel_number = div_element_dealer_tel_number_container.find('div', class_='dp-top__phone')

            # Convert to string
            dealer_tel_number_str = str(div_element_dealer_tel_number)

            # Convert string to array
            dealer_tel_number_arr_raw = dealer_tel_number_str.split(' ')

            # Get the dealers numbers
            dealer_tel_number_1 = dealer_tel_number_arr_raw[5]
            dealer_tel_number_1 = dealer_tel_number_1.split('">')
            dealer_tel_number_1 = dealer_tel_number_1[1]
            dealer_tel_number_1 = dealer_tel_number_1.replace('</a></div>', '')
        
        except AttributeError:
            dealer_name = None
            dealer_email_address = None
            dealer_website = None
            dealer_tel_number_1 = None
            dealer_profile_url = None


        # Open a cursor to perform SQL operationa
        cursor = conn.cursor()

        # Insert data into table
        insert_script = 'INSERT INTO autoscout24_raw (company_name, company_website, company_email_address, company_tel, profile_url, location, advert_url, import_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        insert_values = (dealer_name, dealer_website, dealer_email_address, dealer_tel_number_1, dealer_profile_url, dealer_location, advert_url, import_date)

        # Execute insert script to insert values into the table
        cursor.execute(insert_script, insert_values)

        # Commit execution
        conn.commit()

        counter = counter + 1

        print(f'Records added to database: {counter}')

        # Populate object with dealers info
        # dealers_info = DealersInfo(dealer_location ,advert_url, dealer_profile_url, dealer_name, dealer_email_address, dealer_website, dealer_tel_number_1)

        # Convert python object to json object
        # dealers_info_json = json.dumps(dealers_info.__dict__)

        # Print each object in the terminal
        # print(dealers_info_json)

print(f'Scaping {main_site} - COMPLETE')

conn.close()