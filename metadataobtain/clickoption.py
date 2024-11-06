from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def click_metadata_and_get_info(url):
    # create ChromeOptions objects
    chrome_options = Options()
    # fix Chrome stable version path
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # start ChromeDriver，and fix the Chrome version
    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chrome_options)

    # print Chrome version
    chrome_version = driver.capabilities['browserVersion']
    print(f"now the version of Chrome : {chrome_version}")

    # open target URL
    driver.get(url)

    # print the url title to check if successfully open it
    print(driver.title)

    try:
        # wati for Metadata label and click it
        metadata_tab = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='#datasetForm:tabView:metadataMapTab']"))
        )
        print("Successfully find Metadata label!!!")
        metadata_tab.click()

        # wait and find element contains Persistent Identifier's <td> 
        doi_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//th[contains(text(),'Persistent Identifier')]/following-sibling::td")
            )
        )

        # 
        print(f"DOI content: {doi_element.text}")
        
    except Exception as e:
        print(f"error orrured!: {e}")

    finally:
        # optional:close the website
        driver.quit()
