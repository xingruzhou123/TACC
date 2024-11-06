import requests
import socks
import socket
import json

# URL of the JSON data
url = "https://dataverse.tdl.org/api/datasets/export?exporter=dataverse_json&persistentId=doi%3A10.18738/T8/ZMIWXS"

# Fetching the JSON data from the URL
response = requests.get(url)
data = response.json()

# Set Socks proxy for Neo4j-related proxy configuration
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
socket.socket = socks.socksocket
print("Socks proxy set successfully!")

# Neo4j REST API connection configuration
neo4j_url = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
neo4j_user = "neo4j"
neo4j_password = "12345678"


# Generalized function to extract specified fields
def extract_fields(data, requestdata, datalist, keydata=None, top_level=False):
    if top_level:
        # Handle top-level keys directly under datasetVersion
        if requestdata in data["datasetVersion"]:
            datalist.append(data["datasetVersion"][requestdata])
    else:
        # Handle fields under metadataBlocks->citation->fields
        for field in data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]:
            if field["typeName"] == requestdata:
                if isinstance(field["value"], list) and keydata:  # List of dictionaries
                    for item in field["value"]:
                        datalist.append(item[keydata]["value"])
                elif isinstance(field["value"], list) and not keydata:  # List of strings
                    datalist.extend(field["value"])
                elif isinstance(field["value"], str):  # Single string value
                    datalist.append(field["value"])
def check_instrument_and_human_subjects(data):
    instrument = "empty"
    human_subjects = "no"

    # Scan all description fields to check for the keywords
    description_text = ""
    for field in data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]:
        if field["typeName"] == "description":
            description_text += field["value"] + " "

    # Check for 'instrument' and 'human subject' keywords
    if "instrument" in description_text.lower():
        instrument = "questionnaire"
    if "human subject" in description_text.lower():
        human_subjects = "yes"

    return instrument, human_subjects


# Initialize lists for authors and keywords
research_project_title=[]
team_members = []
research_problem_question = []
study_area=[]
contact_person_and_email=['Maria Esteva','maria@tacc.utexas.edu']
production_date=[]
# Extract title
extract_fields(data, "title", research_project_title, "value")
# Extract author names
extract_fields(data, "author", team_members, "authorName")
# Extract keywords
extract_fields(data, "keyword", research_problem_question, "keywordValue")
#study_area
extract_fields(data, "subject", study_area )
#Production Date 
extract_fields(data, "productionDate", production_date, top_level=True)
#instrument&&human subjects
instrument, human_subjects = check_instrument_and_human_subjects(data)
# Print the results
print("instrument:", instrument)





#the Neo4j main code part
project_data = {
    "research_project_title": ','.join(research_project_title),  # Replace with actual title
    "team_members": ','.join(team_members) ,  # Replace with actual team members
    "research_problem_question": ','.join(research_problem_question),  # Replace with actual research questions
    "study_area": ','.join(study_area),  # Replace with actual study area
    "contact_person_and_email": "Maria Esteva,maria@tacc.utexas.edu",  # Replace with actual contact info
    "production_date": ','.join(production_date),  # Replace with actual production date
    "instrument": instrument,
    "human_subjects": human_subjects
}
# Function to execute a Cypher query via Neo4j REST API
def run_cypher_query(query, params=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    auth = (neo4j_user, neo4j_password)
    payload = {
        "statements": [
            {
                "statement": query,
                "parameters": params or {}
            }
        ]
    }
    response = requests.post(neo4j_url, auth=auth, headers=headers, json=payload)
    if response.status_code == 200:
        print("successful run the cypher")

        return response.json()
    else:
        print(f"Query failed with status {response.status_code}: {response.text}")
        return None

rp_id=[]
# Function to get the maximum rp_id for ResearchProject nodes
def get_max_rp_id():
    query = "MATCH (n:ResearchProject) RETURN n.rp_id AS rp_id ORDER BY rp_id DESC LIMIT 1"
    result = run_cypher_query(query)
    
    if result and "results" in result:
        latest_rp_id = result["results"][0]["data"][0]["row"][0]
        
        # Extract numeric part from rp_id (e.g., "GCR006" -> 6)
        numeric_part = int(latest_rp_id[3:]) if latest_rp_id.startswith("GCR") else 0
        return numeric_part
    return 0

# Function to add ResearchProject node using REST API
def add_research_project_to_neo4j(project_data):
    numeric_rp_idmax = get_max_rp_id()  # Get the max numeric part of rp_id
    new_numeric_rp_id = numeric_rp_idmax + 1  # Increment the numeric part
    new_rp_id = f"GCR{new_numeric_rp_id:03d}"  # Format new rp_id as "GCR" + zero-padded number
    rp_id.append(new_rp_id)
    # Prepare the query to create the node and return the node ID
    query = """
    CREATE (n:ResearchProject {
        rp_id: $rp_id,
        research_project_title: $research_project_title,
        team_members: $team_members,
        research_problem_question: $research_problem_question,
        study_area: $study_area,
        contact_person_and_email: $contact_person_and_email,
        production_date: $production_date,
        instrument: $instrument,
        human_subjects: $human_subjects
    })
    RETURN ID(n) AS node_id
    """
    
    # Prepare parameters for the query
    params = {
        "rp_id": new_rp_id,
        "research_project_title": project_data["research_project_title"],
        "team_members": project_data["team_members"],
        "research_problem_question": project_data["research_problem_question"],
        "study_area": project_data["study_area"],
        "contact_person_and_email": project_data["contact_person_and_email"],
        "production_date": project_data["production_date"],
        "instrument": project_data["instrument"],
        "human_subjects": project_data["human_subjects"]
    }
    
    # Run the query
    result = run_cypher_query(query, params)
    
    # Check and extract the node ID from the result
    if result and "results" in result and result["results"][0]["data"]:
        node_id = result["results"][0]["data"][0]["row"][0]
        print(f"Created ResearchProject with rp_id={new_rp_id} and Neo4j ID={node_id}")
        return node_id
    else:
        print("Failed to create ResearchProject node")
        return None


# Add a new ResearchProject node and retrieve the latest node
#the main node
Grp_id=[]
Grp_id.append(add_research_project_to_neo4j(project_data))
print("Grp_id:",Grp_id)
## find the new node
# MATCH (n:ResearchProject {rp_id: "GCR007"})
# RETURN n

##delete the new code
# MATCH (n:ResearchProject {rp_id: "GCR007"})
# DELETE n

##the research method node
#obtain information
rm_ids=[]
Grm_id=[]
Grm_id1=[]
Grm_id2=[]
def determine_research_method(data):
    # Initialize flags for keyword detection
    found_social = False
    found_robot = False

    # Function to check for keywords in a given text
    def check_keywords(text):
        nonlocal found_social, found_robot
        if "social" in text.lower():
            found_social = True
        if "robot" in text.lower():
            found_robot = True

    # Check the 'description' fields
    for field in data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]:
        if field["typeName"] == "description":
            check_keywords(field["value"])

    # Check the 'title' field
    for field in data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]:
        if field["typeName"] == "title":
            check_keywords(field["value"])

    # Check the 'keyword' fields
    for field in data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]:
        if field["typeName"] == "keyword":
            for keyword in field["value"]:
                check_keywords(keyword["keywordValue"]["value"])

    # Determine the ResearchMethod_name based on found keywords
    research_methods = []
    if found_social:
        research_methods.append("Social Science")
    if found_robot:
        research_methods.append("Experimental")
    if not research_methods:
        research_methods.append("Experimental")  # Default if neither keyword is found

    return research_methods

research_methods = determine_research_method(data)
print("ResearchMethod_name:", research_methods)
# Function to get the maximum rm_id for ResearchMethod nodes
def get_max_rm_id():
    query = "MATCH (n:ResearchMethod) RETURN COALESCE(MAX(n.rm_id), 0) AS rm_idmax"
    result = run_cypher_query(query)
    if result and "results" in result:
        return int(result["results"][0]["data"][0]["row"][0])  # Ensure integer return
    return 0

# Function to create a single ResearchMethod node
# Function to create a single ResearchMethod node
def create_single_research_method_node(research_method):
    rm_idmax = get_max_rm_id()
    new_rm_id = rm_idmax + 1
    rm_ids.append(new_rm_id)
    
    query = """
    CREATE (n:ResearchMethod {
        rm_id: $rm_id,
        name: $name
    })
    RETURN id(n) AS node_id
    """
    
    params = {
        "rm_id": new_rm_id,
        "name": research_method
    }
    
    # Run the query
    result = run_cypher_query(query, params)
    
    # Check and extract the node ID from the result
    if result and "results" in result and result["results"][0]["data"]:
        node_id = result["results"][0]["data"][0]["row"][0]
        print(f"Created ResearchMethod with rm_id={new_rm_id} and Neo4j ID={node_id}")
        return node_id
    else:
        print("Failed to create ResearchMethod node")
        return None


# Function to create two ResearchMethod nodes
def create_double_research_method_nodes(research_method1, research_method2):
    rm_idmax = get_max_rm_id()
    new_rm_id1 = rm_idmax + 1
    new_rm_id2 = rm_idmax + 2
    rm_ids.append(new_rm_id1)
    rm_ids.append(new_rm_id2)
    query1 = """
    CREATE (n:ResearchMethod {
        rm_id: $rm_id,
        name: $name
    })
    """
    params1 = {
        "rm_id": new_rm_id1,
        "name": research_method1
    }
    result1=run_cypher_query(query1, params1)
    # print(f"Created ResearchMethod node with rm_id: {new_rm_id}, name: {research_method}")
    if result1 and "results" in result1 and result1["results"][0]["data"]:
        node_id1 = result1["results"][0]["data"][0]["row"][0]
        print(f"Created Research_method with rm_id={new_rm_id1} and Neo4j ID={node_id1}")
        return node_id1
    else:
        print("Failed to create Research_method node")
        return None
    # print(f"Created ResearchMethod node B1 with rm_id: {new_rm_id1}, name: {research_method1}")

    query2 = """
    CREATE (n:ResearchMethod {
        rm_id: $rm_id,
        name: $name
    })
    """
    params2 = {
        "rm_id": new_rm_id2,
        "name": research_method2
    }
    # run_cypher_query(query2, params2)
    result2=run_cypher_query(query2, params)
    # print(f"Created ResearchMethod node with rm_id: {new_rm_id}, name: {research_method}")
    if result2 and "results" in result1 and result2["results"][0]["data"]:
        node_id2 = result1["results"][0]["data"][0]["row"][0]
        print(f"Created Research_method with rm_id={new_rm_id2} and Neo4j ID={node_id2}")
        return node_id2
    else:
        print("Failed to create Research_method node")
        return None
    # print(f"Created ResearchMethod node B2 with rm_id: {new_rm_id2}, name: {research_method2}")

# Determine and create ResearchMethod node(s)
if len(research_methods) == 1:
    Grm_id.append(create_single_research_method_node(research_methods[0]))
elif len(research_methods) == 2:
    Grm_id1,Grm_id2=create_double_research_method_nodes(research_methods[0], research_methods[1])

##the second layer

def create_unique_relationship(rp_id, rm_id):
    if isinstance(rp_id, list):
        rp_id = rp_id[0]
    if isinstance(rm_id, list):
        rm_id = rm_id[0]
    
    # check if node exists
    query_check_nodes = """
    MATCH (a:ResearchProject {rp_id: $rp_id}), (b:ResearchMethod {rm_id: $rm_id})
    RETURN a, b
    """
    params_check_nodes = {"rp_id": rp_id, "rm_id": rm_id}
    result_check_nodes = run_cypher_query(query_check_nodes, params_check_nodes)
    
    if not result_check_nodes or not result_check_nodes["results"][0]["data"]:
        print(f"cannot find nodes should create node：ResearchProject (rp_id={rp_id}) or ResearchMethod (rm_id={rm_id})first")
        return

    # check whether relationship exists
    query_check_relationship = """
    MATCH (a:ResearchProject {rp_id: $rp_id})-[r:Type]->(b:ResearchMethod {rm_id: $rm_id})
    RETURN r
    """
    result_check_relationship = run_cypher_query(query_check_relationship, params_check_nodes)
    
    if result_check_relationship and result_check_relationship["results"][0]["data"]:
        print("already exist relationship")
        return

    query_create_relationship = """
    MATCH (a:ResearchProject {rp_id: $rp_id}), (b:ResearchMethod {rm_id: $rm_id})
    CREATE (a)-[:Type]->(b)
    RETURN a, b
    """
    result_create_relationship = run_cypher_query(query_create_relationship, params_check_nodes)
    
    if result_create_relationship and result_create_relationship["results"]:
        print(f"Successfully create the relationship with name 'Type'，from ResearchProject (rp_id={rp_id}) to ResearchMethod (rm_id={rm_id})")
    else:
        print("Failed to create the relationship")

create_unique_relationship(rp_id=rp_id, rm_id=rm_ids)

