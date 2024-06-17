from urllib.parse import urlparse
import requests

# Fetch the list of websites
website_list_response = requests.get("http://127.0.0.1:8000/websites/")
website_list = website_list_response.json()

# send a post request
# data = {
#             'company_name': 'SusMafia',
#             'url': urlparse('https://www.susmafia.org/').geturl()
#         }
# print(data)
# response = requests.post("http://127.0.0.1:8000/websites/", data=data)
# print(response)

# companies=""
# for website in website_list:
#     companies+=website['company_name'] + ", "
# print(companies)