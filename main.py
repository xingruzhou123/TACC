# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# import time

# chrome_driver_path = '/usr/local/bin/chromedriver'

# # 设置
# chrome_options = Options()
# chrome_options.add_argument('--headless')  
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.binary_location = '/home/xingru/chrome-126/chrome-linux64/chrome'  

# # 初始化
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # TACC robotics web URL
# url_a = 'https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/UOES4S'

# driver.get(url_a)

# # 等待页面加载完成
# wait = WebDriverWait(driver, 30)

# try:
#     # 等待并点击 "Tree" 按钮
#     tree_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Tree')]")))
#     tree_button.click()
    
#     # 等待 "SceneRecordings" 前面的三角按钮可见并点击
#     scene_recordings_triangle = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'SceneRecordings')]/../preceding-sibling::span[contains(@class, 'fa-caret-right')]")))
#     scene_recordings_triangle.click()
    
#     # 等待目标视频链接出现并获取 URL
#     element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Vid2RealPhase2_P1video')]")))
#     video_url = element.get_attribute('href')
    
#     print(f"Video URL: {video_url}")
    
# except Exception as e:
#     print(f"Cannot find the link: Vid2RealPhase2_P1video, ERROR!: {e}")

# # 关闭浏览器
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')  
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = '/home/xingru/chrome-126/chrome-linux64/chrome'  

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
 
url_a = 'https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/UOES4S'


driver.get(url_a)

time.sleep(15)  


video_urls = {}


for i in range(11, 16):
    video_name = f"Vid2RealPhase2_P{i}video.MP4"
    try:
        
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//a[contains(text(),'{video_name}')]"))
        )
        video_url = element.get_attribute('href')
        video_urls[f"video{i}path"] = video_url
    except Exception as e:
        video_urls[f"video{i}path"] = "empty"
        print(f"cannot find the link: {video_name}, ERROR!: {e}")

driver.quit()

# neo4j command
template = f"""
MATCH (A) WHERE id(A) = 234
MATCH (B:video {{name: "video11", date_file_path: "{video_urls['video11path']}"}})
MATCH (C:video {{name: "video12", date_file_path: "{video_urls['video12path']}"}})
MATCH (D:video {{name: "video13", date_file_path: "{video_urls['video13path']}"}})
MATCH (E:video {{name: "video14", date_file_path: "{video_urls['video14path']}"}})
MATCH (F:video {{name: "video15", date_file_path: "{video_urls['video15path']}"}})
CREATE (A)-[:Dataset_video]->(B)
CREATE (A)-[:Dataset_video]->(C)
CREATE (A)-[:Dataset_video]->(D)
CREATE (A)-[:Dataset_video]->(E)
CREATE (A)-[:Dataset_video]->(F);
"""

print(template)
