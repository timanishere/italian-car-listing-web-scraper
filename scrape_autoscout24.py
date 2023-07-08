# Import json library
import json

# Import beautifulsoup library for webscraping
from bs4 import BeautifulSoup

# Import requests library to request infomation from websites
import requests

#  Configure class
class DealersInfo:
    def __init__(self, location, advert_url, profile_url, company_name):
        self.location = location
        self.advert_url = advert_url
        self.profile_url = profile_url
        self.company_name = company_name
        
# Configure headers to send fake user agent with every request. This fixes 403 response when making a response
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# The main page to scrape from
main_site = 'https://www.autoscout24.it/lst?atype=C&cy=I&damaged_listing=exclude&desc=0&lat=39.21541&lon=9.10932&powertype=kw&search_id=406z74opck&sort=standard&source=listpage_pagination&ustate=N%2CU&zip=cagliari'

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





# Populate object with dealers info
dealers_info = DealersInfo(dealer_location ,advert_url, dealer_profile_url, dealer_name)

# Convert python object to json object
dealers_info_json = json.dumps(dealers_info.__dict__)

# Print each object in the terminal
print(dealers_info_json)