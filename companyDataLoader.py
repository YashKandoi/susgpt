import requests
import csv
import json
from urllib.parse import urlparse

# Fetch the list of websites
website_list_response = requests.get("http://127.0.0.1:8000/websites/")
website_list = website_list_response.json()

# Read data from CSV file, fields are founder_name, company_name, url
with open('company_data.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    count = 0
    for row in csv_reader:
        if count == 0:
            count += 1
            continue
        # if count == 13:
        #     break
        founder_name = row[0]
        company_name = row[1]
        url = row[2]
        count += 1
        flag = 0

        for website in website_list:
            if company_name == website.get('company_name') or url == website.get('url'):
                flag = 1

        if flag == 1:
            print(f"{company_name} is already in the database")
            continue

        data = {
            'company_name': company_name,
            'url': urlparse(url).geturl()
        }
        print(data)
        response = requests.post("http://127.0.0.1:8000/websites/", data=data)
        print(response)