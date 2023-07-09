# Import beautifulsoup library for webscraping
from bs4 import BeautifulSoup

# Import requests library to request infomation from websites
import requests

# Configure headers to send fake user agent with every request. This fixes 403 response when making a response
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# The main page to scrape from
main_site = 'https://www.bakeca.it/annunci/auto/luogo/sardegna/'