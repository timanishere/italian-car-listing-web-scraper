# Import json library
import json

# Import beautifulsoup library for webscraping
from bs4 import BeautifulSoup

# Import requests library to request infomation from websites
import requests

from unidecode import unidecode

#  Configure class
class DealersInfo:
    def __init__(self, location, advert_url, profile_url, company_name, company_email_address, company_website):
        self.location = location
        self.advert_url = advert_url
        self.profile_url = profile_url
        self.company_name = company_name
        self.company_email_address = company_email_address
        self.company_website = company_website
        
# Configure headers to send fake user agent with every request. This fixes 403 response when making a response
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# The main page to scrape from
main_site = 'https://www.autoscout24.it/lst/skoda?atype=C&cy=I&damaged_listing=exclude&desc=0&powertype=kw&search_id=2a7dfxtdq7z&sort=standard&source=homepage_search-mask&ustate=N%2CU'

# Get information from bakeca.it
webpage_1 = requests.get(main_site, headers=HEADERS,).text

# Create instance of beautifulsoup for webpage_1
soup = BeautifulSoup(webpage_1, 'lxml')

# Get advert listing elements
advert_container = soup.find('article', class_='cldt-summary-full-item listing-impressions-tracking list-page-item false ListItem_article__ppamD')

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

# Get name of dealer
dealer_name = soup.find('div', 'CommonComponents_nameContainer__3Z_zp').text
dealer_name = dealer_name.title()

# Get dealers location
dealer_location = soup.find('a', class_='scr-link LocationWithPin_locationItem__pHhCa').text
dealer_location = dealer_location.split(',')
dealer_location = dealer_location[0]
dealer_location = dealer_location.title()
dealer_location = unidecode(dealer_location)

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

# Get raw dealer email address
dealer_email_address_raw = dealer_email_address_arr[3]

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

# Populate object with dealers info
dealers_info = DealersInfo(dealer_location ,advert_url, dealer_profile_url, dealer_name, dealer_email_address, dealer_website)

# Convert python object to json object
dealers_info_json = json.dumps(dealers_info.__dict__)

# Print each object in the terminal
print(dealers_info_json)