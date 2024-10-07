#this script is for obtain the metadata from the  Texas robotics dataverse and generate the node in the neo4j
#now finished:
#1. obtain the title of the website
#2. batch obtain titles from the website 
# 3.obtain the authors 
# 4.obtain the keywords of the page
#
#to-do list
#1. merge the click funtion into this code to click metadata
#2. finish obtain information in related_material, study_area,contact_person_and_email,data_gathering_begin_date,data_gathering_end_date,data_gathering_site,human_subjects
#3. create all above propertires 

import requests
from requests.auth import HTTPBasicAuth
import socks
import socket
from bs4 import BeautifulSoup
import re
import json
from clickoption import click_metadata_and_get_info



# set Socks agents
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
socket.socket = socks.socksocket
print("Socks proxy set successfully!")

# config Neo4j connection information
uri = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
user = "neo4j"
password = "12345678"

# the dataverse url you can replace it to any link(s) you want
urls = [
    "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/0PRYRH",
    "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/ZMIWXS",
    # Add more URLs as needed
]

# for saving the title, authors, and keywords we got
title_matrix = []
author_matrix = []
keywords_matrix = []
info_matrix=[]

# Send a request to fetch the HTML content
for url in urls:
    print(f"Processing URL: {url}")
    # Send a request to fetch the HTML content
    response = requests.get(url)
    # 调用函数并传递 URL 参数
    info_matrix=click_metadata_and_get_info(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the title
        title = soup.find('h1', id='title')
        
        # Find the author (assuming the first part of citation-select span text before a digit)
        citation_span = soup.find('span', class_='citation-select')
        
        # Find keywords (tr with id="keywords")
        keywords_tr = soup.find('tr', id='keywords')
        
        # Processing the title
        if title:
            title_matrix.append([title.get_text()])
            print(f"Title: {title.get_text()}")
        else:
            title_matrix.append(["Title not found"])
            print("Title not found")
        
        # Processing the author
        if citation_span:
            # Extract the text content from the span
            citation_text = citation_span.get_text()

            # Use a regular expression to extract text before the first digit
            match = re.match(r"([^\d]*)", citation_text)
            if match:
                text_before_first_digit = match.group(1).strip()
                print(f"Author: {text_before_first_digit}")
                author_matrix.append([text_before_first_digit])
            else:
                print("No match found")
        else:
            print("Citation span not found")
            author_matrix.append(["Author not found"])

        # Processing the keywords
        if keywords_tr:
            keywords_td = keywords_tr.find('td')
            if keywords_td:
                keywords_text = keywords_td.get_text().strip()
                keywords_matrix.append([keywords_text])
                print(f"Keywords: {keywords_text}")
            else:
                keywords_matrix.append(["Keywords not found"])
                print("Keywords not found")
        else:
            print("Keywords section not found")
            keywords_matrix.append(["Keywords section not found"])
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Function to create a node in Neo4j
def create_neo4j_node(research_project_title, team_members, keywords):
    query = {
        "statements": [{
            "statement": """
                CREATE (n:testnode {
                    research_project_title: $research_project_title,
                    team_members: $team_members,
                    keywords: $keywords
                })
            """,
            "parameters": {
                "research_project_title": research_project_title,
                "team_members": team_members,
                "keywords": keywords
            }
        }]
    }
    
    # send HTTP POST request to Neo4j
    response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)

    # check whether the request to Neo4j is successful
    if response.status_code == 200:
        print(f"Node with title '{research_project_title}' created successfully!")
    else:
        print(f"Failed to create node. Status code: {response.status_code}, Response: {response.text}")
#test to create two nodes r1 and r2

for i in range(len(title_matrix)):  # Ensure we process the node of all url
    research_project_title = title_matrix[i][0]
    team_members = author_matrix[i][0]
    keywords = keywords_matrix[i][0]
    
    # CREATE NODES
    create_neo4j_node(research_project_title, team_members, keywords)

# Output the results (optional)
print("\nTitles:")
for row in title_matrix:
    print(row)

print("\nAuthors:")
for row in author_matrix:
    print(row)

print("\nKeywords:")
for row in keywords_matrix:
    print(row)

print("\info:")
for row in info_matrix:
    print(row)


##this is the test code in Neo4j use 
# DO NOT USE THEM IN PYTHON
# #test tw0 nodes
# MATCH (n:testnode)
# RETURN n.research_project_title, n.team_members, n.keywords
# #delete tw0 nodes
# MATCH (n:testnode)
# DELETE n