import socks
import socket
import requests

from fastapi import FastAPI
from pydantic import BaseModel

# 1) Set the SOCKS5 proxy
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
socket.socket = socks.socksocket
print("Socks proxy set successfully!")

# 2) Neo4j connection info (HTTP REST endpoint)
NEO4J_URI = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

# 3) FastAPI initialization
app = FastAPI()

# Request model for our /run_cypher endpoint
class CypherRequest(BaseModel):
    query: str
    params: dict = {}

@app.post("/run_cypher")
def run_cypher(request: CypherRequest):
    """
    Runs a Cypher query against the Neo4j HTTP REST endpoint
    and returns the results as JSON.
    """
    # The payload follows Neo4j's REST API format
    payload = {
        "statements": [
            {
                "statement": request.query,
                "parameters": request.params
            }
        ]
    }

    # Make the POST request with HTTP Basic Auth
    try:
        response = requests.post(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
            json=payload
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    # Neo4j returns data under "results" -> "data"
    # For reference, the structure looks like:
    # {
    #   "results": [
    #       {
    #           "columns": [...],
    #           "data": [
    #               {"row": [...], "meta": [...]},
    #               ...
    #           ]
    #       }
    #   ],
    #   "errors": [...]
    # }
    result_json = response.json()
    return result_json
