# #this script is for obtain the metadata from the  Texas robotics dataverse and generate the node in the neo4j
# #now finished:
# #1. obtain the title of the website
# #2. batch obtain titles from the website 
# # 3.obtain the authors 
# # 4.obtain the keywords of the page
# #
# #to-do list
# #1. merge the click funtion into this code to click metadata
# #2. finish obtain information in related_material, study_area,contact_person_and_email,data_gathering_begin_date,data_gathering_end_date,data_gathering_site,human_subjects
# #3. create all above propertires 

# ##this is the test code in Neo4j use 
# # DO NOT USE THEM IN PYTHON
# # #test tw0 nodes
# # MATCH (n:testnode)
# # RETURN n.research_project_title, n.team_members, n.keywords
# # #delete tw0 nodes
# # MATCH (n:testnode)
# # DELETE n
# import socks
# import socket
# from bs4 import BeautifulSoup
# import re
# import requests
# from requests.auth import HTTPBasicAuth
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from clickoption import click_metadata_and_get_info  # Assuming this is your custom method

# # Set up Chrome options
# chrome_options = Options()
# # You can run Chrome in headless mode (optional)
# # chrome_options.add_argument("--headless")

# # Provide the path to ChromeDriver
# service = Service("/usr/local/bin/chromedriver")

# try:
#     # Initialize the Chrome WebDriver
#     driver = webdriver.Chrome(service=service, options=chrome_options)
# except Exception as e:
#     print(f"Failed to initialize the WebDriver. Error: {str(e)}")
#     exit(1)

# # set Socks agents for Neo4j-related proxy configuration
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
# socket.socket = socks.socksocket
# print("Socks proxy set successfully!")

# # config Neo4j connection information
# uri = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
# user = "neo4j"
# password = "12345678"

# # List of Dataverse URLs to process
# urls = [
#     "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/0PRYRH",
#     "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/ZMIWXS",
#     # Add more URLs as needed
# ]

# # Containers to hold results
# title_matrix = []
# author_matrix = []
# keywords_matrix = []
# info_matrix = []

# # Iterate through URLs
# for url in urls:
#     print(f"Processing URL: {url}")
#     try:
#         # Open the webpage with Selenium
#         driver.get(url)
        
#         # Wait for the page to load (optional if needed)
#         driver.implicitly_wait(5)  # Adjust time if needed
        
#         # Get page source after loading
#         page_source = driver.page_source
        
#         # Use BeautifulSoup to parse the HTML content
#         soup = BeautifulSoup(page_source, 'html.parser')
        
#         # Find the title, author, and keywords
#         title = soup.find('h1', id='title')
#         citation_span = soup.find('span', class_='citation-select')
#         keywords_tr = soup.find('tr', id='keywords')

#         # Process and store title
#         if title:
#             title_matrix.append([title.get_text()])
#             print(f"Title: {title.get_text()}")
#         else:
#             title_matrix.append(["Title not found"])
#             print("Title not found")

#         # Process and store author
#         if citation_span:
#             citation_text = citation_span.get_text()
#             match = re.match(r"([^\d]*)", citation_text)
#             if match:
#                 text_before_first_digit = match.group(1).strip()
#                 author_matrix.append([text_before_first_digit])
#                 print(f"Author: {text_before_first_digit}")
#             else:
#                 author_matrix.append(["Author not found"])
#                 print("No author found")
#         else:
#             author_matrix.append(["Author not found"])
#             print("Citation span not found")

#         # Process and store keywords
#         if keywords_tr:
#             keywords_td = keywords_tr.find('td')
#             if keywords_td:
#                 keywords_text = keywords_td.get_text().strip()
#                 keywords_matrix.append([keywords_text])
#                 print(f"Keywords: {keywords_text}")
#             else:
#                 keywords_matrix.append(["Keywords not found"])
#                 print("Keywords not found")
#         else:
#             keywords_matrix.append(["Keywords section not found"])
#             print("Keywords section not found")
#     except Exception as e:
#         print(f"Failed to process URL {url}. Error: {str(e)}")
#         title_matrix.append(["Processing error"])
#         author_matrix.append(["Processing error"])
#         keywords_matrix.append(["Processing error"])

# # Function to create a node in Neo4j
# def create_neo4j_node(research_project_title, team_members, keywords):
#     query = {
#         "statements": [{
#             "statement": """
#                 CREATE (n:testnode {
#                     research_project_title: $research_project_title,
#                     team_members: $team_members,
#                     keywords: $keywords
#                 })
#             """,
#             "parameters": {
#                 "research_project_title": research_project_title,
#                 "team_members": team_members,
#                 "keywords": keywords
#             }
#         }]
#     }
    
#     # Send HTTP POST request to Neo4j
#     response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)

#     # Check whether the request to Neo4j is successful
#     if response.status_code == 200:
#         print(f"Node with title '{research_project_title}' created successfully!")
#     else:
#         print(f"Failed to create node. Status code: {response.status_code}, Response: {response.text}")

# # Create nodes in Neo4j for each dataset
# for i in range(len(title_matrix)):  # Ensure we process the node for all URLs
#     research_project_title = title_matrix[i][0]
#     team_members = author_matrix[i][0]
#     keywords = keywords_matrix[i][0]
    
#     # CREATE NODES
#     create_neo4j_node(research_project_title, team_members, keywords)

# # Output the results (optional)
# print("\nTitles:")
# for row in title_matrix:
#     print(row)

# print("\nAuthors:")
# for row in author_matrix:
#     print(row)

# print("\nKeywords:")
# for row in keywords_matrix:
#     print(row)

import socks
import socket
from bs4 import BeautifulSoup
import re
import time
import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from clickoption import click_metadata_and_get_info  


chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome"  # Adjust if the binary is in a different path
chrome_options.add_argument("--headless")  # Optional: Run in headless mode

# Explicitly set the path to ChromeDriver
service = Service("/usr/local/bin/chromedriver")

try:
    # Initialize the Chrome WebDriver with the service and options explicitly
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com")
    print(driver.title)  # Should print "Google"
    driver.quit()
except Exception as e:
    print(f"Failed to initialize the WebDriver. Error: {str(e)}")
    exit(1)

# set Socks agents for Neo4j-related proxy configuration
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
socket.socket = socks.socksocket
print("Socks proxy set successfully!")

# config Neo4j connection information
uri = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
user = "neo4j"
password = "12345678"

# List of Dataverse URLs to process
urls = [
    "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/0PRYRH",
    "https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/ZMIWXS",
    # Add more URLs as needed
]

# Containers to hold results
title_matrix = []
author_matrix = []
keywords_matrix = []
info_matrix = []

# Iterate through URLs
for url in urls:
    print(f"Processing URL: {url}")
    try:
        # Open the webpage with Selenium
        driver.get(url)
        
        # Wait for the page to load (optional if needed)
        driver.implicitly_wait(5)  # Adjust time if needed
        
        # Get page source after loading
        page_source = driver.page_source
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Optional: Get additional metadata with your custom method
        try:
            info_matrix.append(click_metadata_and_get_info(url))
        except Exception as e:
            print(f"Error with custom method click_metadata_and_get_info: {str(e)}")
            info_matrix.append("Info not found")
        
        # Find the title, author, and keywords
        title = soup.find('h1', id='title')
        citation_span = soup.find('span', class_='citation-select')
        keywords_tr = soup.find('tr', id='keywords')

        # Process and store title
        if title:
            title_matrix.append([title.get_text()])
            print(f"Title: {title.get_text()}")
        else:
            title_matrix.append(["Title not found"])
            print("Title not found")

        # Process and store author
        if citation_span:
            citation_text = citation_span.get_text()
            match = re.match(r"([^\d]*)", citation_text)
            if match:
                text_before_first_digit = match.group(1).strip()
                author_matrix.append([text_before_first_digit])
                print(f"Author: {text_before_first_digit}")
            else:
                author_matrix.append(["Author not found"])
                print("No author found")
        else:
            author_matrix.append(["Author not found"])
            print("Citation span not found")

        # Process and store keywords
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
            keywords_matrix.append(["Keywords section not found"])
            print("Keywords section not found")

        # Check for 'human subjects' term in the page
        if 'human subjects' in page_source.lower():
            print("HumanSubjects exists")
            # Find current max hs_id in Neo4j
            query = {
                "statements": [{
                    "statement": "MATCH (n:HumanSubjects) RETURN MAX(n.hs_id) AS max_hs_id"
                }]
            }
            response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
            if response.status_code == 200:
                max_hs_id = response.json()['results'][0]['data'][0]['row'][0] or 0
                hs_id = max_hs_id + 1
                # Create HumanSubjects node and relationship
                query = {
                    "statements": [{
                        "statement": """
                            MATCH (a:ResearchProject {research_project_title: $research_project_title})
                            CREATE (b:HumanSubjects {hs_id: $hs_id, name: 'HumanSubjects', age: null, gender: null})
                            CREATE (a)-[:Has_Subclass]->(b)
                        """,
                        "parameters": {
                            "research_project_title": title_matrix[-1][0],
                            "hs_id": hs_id
                        }
                    }]
                }
                response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
                if response.status_code == 200:
                    print(f"HumanSubjects node with hs_id {hs_id} created successfully!")
                else:
                    print(f"Failed to create HumanSubjects node. Status code: {response.status_code}, Response: {response.text}")

        # Create Session node and relationship
        query = {
            "statements": [{
                "statement": "MATCH (n:Session) RETURN MAX(n.s_id) AS max_s_id"
            }]
        }
        response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
        if response.status_code == 200:
            max_s_id = response.json()['results'][0]['data'][0]['row'][0] or 0
            s_id = max_s_id + 1
            query = {
                "statements": [{
                    "statement": """
                        MATCH (a:ResearchProject {research_project_title: $research_project_title})
                        CREATE (b:Session {s_id: $s_id, name: 'Session'})
                        CREATE (a)-[:Has_Subclass]->(b)
                    """,
                    "parameters": {
                        "research_project_title": title_matrix[-1][0],
                        "s_id": s_id
                    }
                }]
            }
            response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
            if response.status_code == 200:
                print(f"Session node with s_id {s_id} created successfully!")
            else:
                print(f"Failed to create Session node. Status code: {response.status_code}, Response: {response.text}")

        # Create ExperimentSetting node and relationship
        query = {
            "statements": [{
                "statement": "MATCH (n:ExperimentSetting) RETURN MAX(n.se_id) AS max_se_id"
            }]
        }
        response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
        if response.status_code == 200:
            max_se_id = response.json()['results'][0]['data'][0]['row'][0] or 0
            se_id = max_se_id + 1
            query = {
                "statements": [{
                    "statement": """
                        MATCH (a:ResearchProject {research_project_title: $research_project_title})
                        CREATE (b:ExperimentSetting {se_id: $se_id, name: 'ExperimentSetting'})
                        CREATE (a)-[:Has_Subclass]->(b)
                    """,
                    "parameters": {
                        "research_project_title": title_matrix[-1][0],
                        "se_id": se_id
                    }
                }]
            }
            response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
            if response.status_code == 200:
                print(f"ExperimentSetting node with se_id {se_id} created successfully!")
            else:
                print(f"Failed to create ExperimentSetting node. Status code: {response.status_code}, Response: {response.text}")

        # Create ExperimentInstrument node and relationship
        query = {
            "statements": [{
                "statement": "MATCH (n:ExperimentInstrument) RETURN MAX(n.hs_id) AS max_hs_id"
            }]
        }
        response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
        if response.status_code == 200:
            max_hs_id = response.json()['results'][0]['data'][0]['row'][0] or 0
            hs_id = max_hs_id + 1
            query = {
                "statements": [{
                    "statement": """
                        MATCH (a:ResearchProject {research_project_title: $research_project_title})
                        CREATE (b:ExperimentInstrument {hs_id: $hs_id, name: 'ExperimentInstrument'})
                        CREATE (a)-[:Has_Subclass]->(b)
                    """,
                    "parameters": {
                        "research_project_title": title_matrix[-1][0],
                        "hs_id": hs_id
                    }
                }]
            }
            response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)
            if response.status_code == 200:
                print(f"ExperimentInstrument node with hs_id {hs_id} created successfully!")
            else:
                print(f"Failed to create ExperimentInstrument node. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"Failed to process URL {url}. Error: {str(e)}")
        title_matrix.append(["Processing error"])
        author_matrix.append(["Processing error"])
        keywords_matrix.append(["Processing error"])
        info_matrix.append("Processing error")

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
    
    # Send HTTP POST request to Neo4j
    response = requests.post(uri, auth=HTTPBasicAuth(user, password), json=query)

    # Check whether the request to Neo4j is successful
    if response.status_code == 200:
        print(f"Node with title '{research_project_title}' created successfully!")
    else:
        print(f"Failed to create node. Status code: {response.status_code}, Response: {response.text}")

# Create nodes in Neo4j for each dataset
for i in range(len(title_matrix)):  # Ensure we process the node for all URLs
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

print("\nInfo:")
for row in info_matrix:
    print(row)
