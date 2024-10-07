import os
from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Dataverse
import requests

base_url = 'https://dataverse.tdl.org/'
api_token = "879ee754-8e08-48a4-86c1-f12c9f208d10"
api = NativeApi(base_url, api_token)
data_api = DataAccessApi(base_url)

DOI = "doi:10.18738/T8/ZMIWXS"
dataset = api.get_dataset(DOI)

if not os.path.exists("random_mdps"):
    os.makedirs("random_mdps")
if not os.path.exists("delivery_mdp"):
    os.makedirs("delivery_mdp")

files_list = dataset.json()['data']['latestVersion']['files']
for file in files_list:
    filename = file["dataFile"]["filename"]
    file_id = file["dataFile"]["id"]
    print(f"Downloading: File name {filename}, id {file_id}")

    # Construct the download URL
    download_url = f"{base_url}api/access/datafile/{file_id}"

    # Set up the request headers with the API token
    headers = {'X-Dataverse-key': api_token}

    try:
        # Use requests to download the file
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Determine the directory
        dir = "delivery_mdp/" if "DELIVERY" in filename else "random_mdps/"

        # Save the file
        with open(os.path.join(dir, filename), "wb") as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {filename}")

    except requests.RequestException as e:
        print(f"Error downloading {filename}: {str(e)}")

print("Download process completed.")
