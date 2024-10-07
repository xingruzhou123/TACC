# import requests
# from requests.auth import HTTPBasicAuth
# import socks
# import socket
# import csv

# # 设置Socks代理
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
# socket.socket = socks.socksocket
# print("Socks proxy set successfully!")

# # 配置你的Neo4j连接信息
# uri = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
# user = "neo4j"
# password = "12345678"

# # 定义Cypher查询

# query = {
#     "statements": [
#         {
#             "statement": """
#             MATCH (n)-[r]-(connected)
#             WHERE id(n) IN [28,60,63,65,66,67,69,72,74,212,213,214,215,224,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412]
#             RETURN id(n) AS nodeID, labels(n) AS nodeLabels, properties(n) AS nodeProperties,
#                    id(connected) AS connectedNodeID, labels(connected) AS connectedNodeLabels, properties(connected) AS connectedNodeProperties,
#                    type(r) AS relationshipType, properties(r) AS relationshipProperties
#             """
#         }
#     ]
# }

# # 发送HTTP请求
# try:
#     response = requests.post(uri, json=query, auth=HTTPBasicAuth(user, password))
#     response.raise_for_status()  # 检查是否有HTTP错误
#     results = response.json()
#     print("Query results received.")
    

#     # 解析结果并保存为TXT文件
#     with open('connected_nodes.txt', mode='w') as txt_file:
#         for result in results['results']:
#             data = result['data']
#             for row in data:
#                 txt_file.write(f"Node ID: {row['row'][0]}\n")
#                 txt_file.write(f"Node Labels: {', '.join(row['row'][1])}\n")
#                 txt_file.write(f"Node Properties: {row['row'][2]}\n")
#                 txt_file.write(f"Connected Node ID: {row['row'][3]}\n")
#                 txt_file.write(f"Connected Node Labels: {', '.join(row['row'][4])}\n")
#                 txt_file.write(f"Connected Node Properties: {row['row'][5]}\n")
#                 txt_file.write(f"Relationship Type: {row['row'][6]}\n")
#                 txt_file.write(f"Relationship Properties: {row['row'][7]}\n")
#                 txt_file.write(f"Relationship between Node ID {row['row'][0]} and Connected Node ID {row['row'][3]}\n")
#                 txt_file.write("-" * 40 + "\n")
#     print("Results saved to connected_nodes.txt")

# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")
import requests
from requests.auth import HTTPBasicAuth
import socks
import socket
import subprocess
import re

# 设置Socks代理
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 5555)
socket.socket = socks.socksocket
print("Socks proxy set successfully!")

# 配置你的Neo4j连接信息
uri = "http://robotics-datamodel.tacc.utexas.edu:7474/db/neo4j/tx/commit"
user = "neo4j"
password = "12345678"

# 运行 calculate.py 并获取输出
output = subprocess.check_output(['python3', 'calculate.py']).decode('utf-8')
print("Output from calculate.py:", output)

# 解析 calculate.py 的输出
number_match = re.search(r'number\[(.*?)\]', output)
if number_match:
    number_str = number_match.group(1)
    number_list = list(map(int, number_str.split(',')))
else:
    print("Error: Could not find 'number' in the output")
    number_list = []

print("Parsed number list:", number_list)

# 定义Cypher查询
query = {
    "statements": [
        {
            "statement": f"""
            MATCH (n)-[r]-(connected)
            WHERE id(n) IN {number_list}
            RETURN id(n) AS nodeID, labels(n) AS nodeLabels, properties(n) AS nodeProperties,
                   id(connected) AS connectedNodeID, labels(connected) AS connectedNodeLabels, properties(connected) AS connectedNodeProperties,
                   type(r) AS relationshipType, properties(r) AS relationshipProperties
            """
        }
    ]
}

# 发送HTTP请求
try:
    response = requests.post(uri, json=query, auth=HTTPBasicAuth(user, password))
    response.raise_for_status()  # 检查是否有HTTP错误
    results = response.json()
    print("Query results received.")
    
    # 解析结果并保存为TXT文件
    with open('connected_nodes.txt', mode='w') as txt_file:
        for result in results['results']:
            data = result['data']
            for row in data:
                txt_file.write(f"Node ID: {row['row'][0]}\n")
                txt_file.write(f"Node Labels: {', '.join(row['row'][1])}\n")
                txt_file.write(f"Node Properties: {row['row'][2]}\n")
                txt_file.write(f"Connected Node ID: {row['row'][3]}\n")
                txt_file.write(f"Connected Node Labels: {', '.join(row['row'][4])}\n")
                txt_file.write(f"Connected Node Properties: {row['row'][5]}\n")
                txt_file.write(f"Relationship Type: {row['row'][6]}\n")
                txt_file.write(f"Relationship Properties: {row['row'][7]}\n")
                txt_file.write(f"Relationship between Node ID {row['row'][0]} and Connected Node ID {row['row'][3]}\n")
                txt_file.write("-" * 40 + "\n")
    print("Results saved to connected_nodes.txt")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
