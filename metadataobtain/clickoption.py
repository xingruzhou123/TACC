# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC


# # 创建 ChromeOptions 对象
# chrome_options = Options()

# # 指定 Chrome 正式版的路径 (129版本)
# chrome_options.binary_location = "/usr/bin/google-chrome"  # 替换为正式版 Chrome 的路径
# chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
# chrome_options.add_argument("--no-sandbox")   # 禁用沙盒模式
# # 启动 ChromeDriver，并指定 Chrome 版本
# driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chrome_options)
# chrome_version = driver.capabilities['browserVersion']
# print(f"当前 Chrome 浏览器的版本是: {chrome_version}")
# driver.get("https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/ZMIWXS")

# # 可选：打印当前页面的标题，以验证是否成功打开
# print(driver.title)
# try:
#     metadata_tab = WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.XPATH, "//a[@href='#datasetForm:tabView:metadataMapTab']"))
#     )
#     print("Metadata 标签找到！")
#     metadata_tab.click()  # 点击 Metadata 标签

#     # 等待并查找包含 Persistent Identifier 的 <td> 元素
#     doi_element = WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//th[contains(text(),'Persistent Identifier')]/following-sibling::td")
#         )
#     )

#     # 输出 DOI 内容
#     print(f"DOI 字段内容: {doi_element.text}")
    
# except Exception as e:
#     print(f"出现错误: {e}")
# except Exception as e:
#     print(f"找不到 Metadata 标签: {e}")


# # 可选：关闭浏览器
# # driver.quit()
# clickoption.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def click_metadata_and_get_info(url):
    # 创建 ChromeOptions 对象
    chrome_options = Options()
    # 指定 Chrome 正式版的路径
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # 启动 ChromeDriver，并指定 Chrome 版本
    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chrome_options)

    # 打印 Chrome 浏览器的版本
    chrome_version = driver.capabilities['browserVersion']
    print(f"当前 Chrome 浏览器的版本是: {chrome_version}")

    # 打开指定的 URL
    driver.get(url)

    # 打印当前页面的标题，以验证是否成功打开
    print(driver.title)

    try:
        # 等待 Metadata 标签并点击
        metadata_tab = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='#datasetForm:tabView:metadataMapTab']"))
        )
        print("Metadata 标签找到！")
        metadata_tab.click()

        # 等待并查找包含 Persistent Identifier 的 <td> 元素
        doi_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//th[contains(text(),'Persistent Identifier')]/following-sibling::td")
            )
        )

        # 输出 DOI 内容
        print(f"DOI 字段内容: {doi_element.text}")
        
    except Exception as e:
        print(f"出现错误: {e}")

    finally:
        # 可选：关闭浏览器
        driver.quit()
