# Import json library
import json

# Import beautifulsoup library for webscraping
from bs4 import BeautifulSoup

# Import requests library to request infomation from websites
import requests

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
    def __init__(self, location, advert_url, profile_url, company_name, company_email_address, company_website, company_tel_1, import_date):
        self.location = location
        self.advert_url = advert_url
        self.profile_url = profile_url
        self.company_name = company_name
        self.company_email_address = company_email_address
        self.company_website = company_website
        self.company_tel_1 = company_tel_1
        self.import_date = import_date

# Configure headers to send fake user agent with every request. This fixes 403 response when making a response
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# The main page to scrape from
main_site = 'https://www.bakeca.it/annunci/auto/luogo/sardegna/'

# Set import date as the current day
import_date = date.today()

# Get information from bakeca.it
webpage_1 = requests.get(main_site, headers=HEADERS,).text

# Print messsage in terminal to know that scraping is in progress
print(f'Scaping {main_site} in progress...')

# Create instance of beautifulsoup for webpage_1
soup = BeautifulSoup(webpage_1, 'lxml')

# Create an empty array to store raw dealer info
dealers_info_json_arr_raw = []

try:
    # Get paginator
    paginator_container = soup.find('div', class_ = 'bg-white flex-1 flex items-center py-4 w-full footer-paginator')

    # Get element containing number of pages
    number_of_pages_element = paginator_container.find('span', class_ = 'text-slate-700 mx-auto')

    # Convert element into a string
    number_of_pages_element_str = str(number_of_pages_element)

    # Convert element into an array
    number_of_pages_element_arr = number_of_pages_element_str.split(' ')

    # Get the last number of the page
    last_page_raw = number_of_pages_element_arr[5]

    # Clean string to get number
    last_page = last_page_raw.replace('<strong>', '')
    last_page = last_page.replace('</strong></span>', '')
    last_page = int(last_page)
    last_page = last_page + 1
except AttributeError:
    last_page = 1 + 1

counter = 0 

for i in range(1, last_page):

    i = str(i)

    # The main page to scrape from
    main_site_loop = main_site + '/page/' + i + '/'

    # Get information from bakeca.it
    webpage_loop = requests.get(main_site_loop, headers=HEADERS,).text

    # Create instance of beautifulsoup for webpage_1
    soup = BeautifulSoup(webpage_loop, 'lxml')

    # Get advert listing elements
    advert_containers = soup.findAll('div', class_='cursor-pointer border-b relative p-3 tablet:px-0 -mx-3 mobile:mx-0 annuncio-in-elenco bg-white',)

    for advert_container in advert_containers:

        # Get dealers location
        dealer_location = advert_container.find('span', class_='text-sm text-slate-700 truncate block px-3').text
        dealer_location = dealer_location.title()

        # Get advert url
        a_element_advert_url = advert_container.find('a', class_='flex relative')

        # Convert object to string
        a_element_advert_url_str = str(a_element_advert_url)

        # Convert string to array
        a_element_advert_url_arr = a_element_advert_url_str.split(' ')

        # Get raw advert url
        advert_url_raw = a_element_advert_url_arr[3]

        # Clean raw data to get URL
        advert_url = advert_url_raw.replace('href="', '')
        advert_url = advert_url.replace('?from-premium"><div', '')
        advert_url = advert_url.replace('"><div', '')
        
        # Get URL of dealer page
        span_element_dealer_info = advert_container.find('span', class_='z-10 tablet:mt-3 relative block leading-tight text-sm hover:underline truncate text-slate-700 w-auto')

        # Convert object to string
        span_element_dealer_info_str = str(span_element_dealer_info)

        # Convert string to array
        span_element_dealder_info_arr = span_element_dealer_info_str.split(' ')

        # If a dealer has a profile url, run code to get profile url
        try:
            # Get raw format of the dealers profile url
            dealer_profile_url_raw = span_element_dealder_info_arr[17]
            
            # Clean raw data to get URL
            dealer_profile_url_raw = dealer_profile_url_raw.replace("window.location.href='", "")
            dealer_profile_url_raw = dealer_profile_url_raw.replace("/'", "")
            dealer_profile_url = dealer_profile_url_raw.replace('">Concessionario:', '')
            dealer_profile_url = dealer_profile_url.replace('">Azienda:', '')
        
            # Get information from dealer profile
            webpage_2 = requests.get(dealer_profile_url, headers=HEADERS,).text

            # Create instance of beautifulsoup for webpage_2
            soup = BeautifulSoup(webpage_2, 'lxml')

            # Get Name of dealer
            dealer_name = soup.find('h1', 'b-vetrina-titolo').text
            dealer_name = dealer_name.replace('\n', '')
            dealer_name = dealer_name[:-1]
            dealer_name = dealer_name.title()

            # Get contact details from dealer profile
            ul_dealer_contact_details = soup.find('ul',class_='b-vetrina-info')

            # Get all <li> elements from the dealers contact info
            li_dealer_contact_info = ul_dealer_contact_details.findAll('li')

            # Get <li> element containing the dealer telephone number
            li_dealer_tel_number = li_dealer_contact_info[0]

            # Convert <li> to string
            dealer_tel_number_str = str(li_dealer_tel_number)

            # Convert string to array
            dealer_tel_number_arr_raw = dealer_tel_number_str.split(' ')

            # Initalize empty array to store tel numbers
            dealer_tel_number_arr_clean = []

            # Start looping through array
            for item in dealer_tel_number_arr_raw:

                # Check if each item contains a digit
                if item.isdigit():

                    # Append number to the clean array if they contain a digit
                    dealer_tel_number_arr_clean.append(item)
            
            # Get the dealers numbers
            dealer_tel_number_1 = dealer_tel_number_arr_clean[0]
            # dealer_tel_number_2 = dealer_tel_number_arr_clean[1]
            # dealer_tel_number_3 = dealer_tel_number_arr_clean[2]

            # Get <li> element containing the dealers email
            li_dealer_email_address = li_dealer_contact_info[1]

            # Convert <li> to string
            dealer_email_address_str = str(li_dealer_email_address)

            # Convert string to array
            dealer_email_address_arr_raw = dealer_email_address_str.split(' ')

            # Get encrypted email address
            dealer_encrypted_email_address_raw = dealer_email_address_arr_raw[5]

            # Clean encrypted email address
            dealer_encrypted_email_address = dealer_encrypted_email_address_raw.replace('data-cfemail="', '')
            dealer_encrypted_email_address = dealer_encrypted_email_address.replace('"', '')

            # Create a function to decode the email address 
            def decodeEmailAddress(encodedString):
                r = int(encodedString[:2],16)
                dealer_email_address = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
                
                return dealer_email_address

            # Decode email address
            dealer_email_address = decodeEmailAddress(dealer_encrypted_email_address)

            # Get <li> element containing the dealers website
            li_dealer_website = li_dealer_contact_info[2]

            # Convert <li> to string
            dealer_website_str = str(li_dealer_website)

            # Convert string to array
            dealer_website_arr_raw = dealer_website_str.split(' ')

            # Get website raw
            dealer_website_raw = dealer_website_arr_raw[5]

            # Clean website raw
            dealer_website = dealer_website_raw.replace('href="', '')
            dealer_website = dealer_website.replace('"', '')

            
        # If dealer doesn't have profile url, set to None
        except IndexError:
            dealer_profile_url_raw = None
            dealer_profile_url = None
            dealer_name = None
            dealer_email_address = None
            dealer_website = None
            dealer_tel_number_1 = None

        # Open a cursor to perform SQL operationa
        cursor = conn.cursor()

        # Insert data into table
        insert_script = 'INSERT INTO bakeca_raw (company_name, company_website, company_email_address, company_tel, profile_url, location, advert_url, import_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        insert_values = (dealer_name, dealer_website, dealer_email_address, dealer_tel_number_1, dealer_profile_url, dealer_location, advert_url, import_date)

        # Execute insert script to insert values into the table
        cursor.execute(insert_script, insert_values)

        # Commit execution
        conn.commit()

        # Populate object with dealers info
        # dealers_info = DealersInfo(dealer_location, advert_url, dealer_profile_url, dealer_name, dealer_email_address, dealer_website, dealer_tel_number_1)
        
        counter = counter + 1

        print(f'Records added to database: {counter}')

        # Convert python object to json object
        # dealers_info_json = json.dumps(dealers_info.__dict__)

        # Print each object in the terminal
        # print(dealers_info_json)
        
        # Append each object into the array
        # dealers_info_json_arr_raw.append(dealers_info_json)

    # print(dealers_info_json_arr_raw)
print(f'Scaping {main_site} - COMPLETE')

conn.close()
    