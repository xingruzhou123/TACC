#this python script is used to save pics in the Robotics Dataverse
#However, it is not required in this stage
#so, this script is not really used in th project
#and this script did not use <class> to classify different pics
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# Configure Chrome options for headless browsing
chrome_driver_path = '/usr/local/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')  
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = '/home/xingru/chrome-126/chrome-linux64/chrome'  

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the webpage to scrape
url_a = 'https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/UOES4S'
driver.get(url_a)

# Wait for the page to load completely
time.sleep(5)

# Ensure the "Read full Description[+]" button is visible and clickable
try:
    read_more_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Read full Description[+]')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", read_more_button)
    driver.execute_script("arguments[0].click();", read_more_button)
    print("Clicked 'Read full Description[+]' button.")
except Exception as e:
    print(f"Error clicking 'Read full Description[+]': {e}")
    driver.quit()
    exit()

# Wait for the full description to load
time.sleep(5)

# Create a directory to save the images
if not os.path.exists('images'):
    os.makedirs('images')

try:
    # Locate the sections of interest: from "Introduction" to "Acknowledgement"
    introduction_section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Introduction')]")
    acknowledgement_section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Acknowledgement')]")

    # Get the images between the "Introduction" and "Acknowledgement" sections
    images_within_section = introduction_section.find_elements(By.XPATH, ".//following::img[preceding::h2[contains(text(), 'Acknowledgement')]]")

    # Save each image
    for index, img in enumerate(images_within_section):
        img_url = img.get_attribute('src')
        if img_url:
            # Generate the filename
            filename = f"subtitlename{index + 1}.png"
            filepath = os.path.join('images', filename)
            
            # Download and save the image
            try:
                response = requests.get(img_url)
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f"Saved image {filename}")
            except Exception as e:
                print(f"Failed to save image {index + 1}: {e}")

except Exception as e:
    print(f"Error finding sections or images: {e}")

# Close the browser
driver.quit()

# Print completion message
print("Images between 'Introduction' and 'Acknowledgement' have been saved successfully.")
