import re
from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import Website
from .serializers import WebsiteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Extract button links from output
def extract_links(content):
    # Find the "Links/Buttons:" section
    links_section_start = content.find("Links/Buttons:")
    
    # If the section is found
    if links_section_start != -1:
        # Extract the content of the "Links/Buttons:" section
        links_content = content[links_section_start:]
        
        # Use regex to find all links within the "Links/Buttons:" section
        links = re.findall(r'\((https?://[^\)]+)\)', links_content)
        
        return links
    else:
        return []

# JINA API function call
def scrape_website(url):
    try:
        headers = { "X-With-Generated-Alt": "true",
                    "X-With-Links-Summary": "true",
                    "X-With-Images-Summary": "true",
                    "X-No-Cache": "true",
                    "X-Target-Selector": "#img-content",
                    "X-Wait-For-Selector": "#content"
                     }
        # Layer 1 response
        response = requests.get("https://r.jina.ai/" + url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        links = extract_links(response.text)
        output=response.text + "\n"
        # extract the name of the company from the url, Example: http://neufin.com, output: neufin
        company_name = url.split("//")[1].split(".")[0]
        company_name = company_name.lower()
        # if company name more than 1 letter add - in between words
        company_name2=""
        if len(company_name) > 1:
            company_name2 = company_name.replace(" ", "-")
        # Layer 2 response
        for link in links:
            if (company_name) in link or (company_name2) in link:
                response = requests.get("https://r.jina.ai/" + link, headers=headers)
                response.raise_for_status()
                output += response.text + "\n"
        output += "Total number of characters: " + str(len(output))
        return output
    except requests.RequestException as e:
        return {'error': str(e)}


@api_view(['GET','POST'])
def Website_List(request,format=None):

    if request.method == 'GET':
        output = [{"company_name": output.company_name, "url": output.url, "output": output.output}
                  for output in Website.objects.all()]
        # websites = Website.objects.all()
        # serializer = WebsiteSerializer(websites, many=True)
        # return Response(serializer.data)
        return Response(output)

    elif request.method == 'POST':
        serializer = WebsiteSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the company name already exists in the database
            if Website.objects.filter(company_name=request.data['company_name']).exists():
                return Response("Company name already exists", status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            response = scrape_website(request.data['url'])
            serializer.validated_data['output'] = response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def Website_Detail(request, company_name,format=None):
    try:    
        website = Website.objects.get(company_name=company_name)
    except Website.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WebsiteSerializer(website, many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = WebsiteSerializer(website, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # getting JINA API to work here
            response = scrape_website(website.url)
            website.output = response
            website.save()
            
            serializer.data['output'] = response
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def home(request):
    return render(request,'homepage.html')