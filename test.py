from urllib.parse import urlparse
import requests

# Fetch the list of websites
website_list_response = requests.get("http://127.0.0.1:8000/websites/")
website_list = website_list_response.json()
