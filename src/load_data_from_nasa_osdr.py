# import os
# import shutil
# import time
# import zipfile
# from urllib.parse import urlparse
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_autoinstaller
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager  # 自動管理 chromedriver 版本
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.opera import OperaDriverManager
# from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver

# # 設定主要下載路徑(例如桌面的 NASA_OSDR_Downloads/zip files 資料夾)
# main_download_path = os.path.join(os.path.expanduser("~"), "Desktop", "NASA_OSDR_Downloads", "zip files")

# # 設定預設解壓縮路徑(例如桌面的 NASA_OSDR_Downloads/ 資料夾)
# extract_files_path = os.path.join(os.path.expanduser("~"), "Desktop", "NASA_OSDR_Downloads")

# # 定義下載資料的函數
# def load_data_from_nasa_osdr_app(user_input_url, web_browser_type):
#     try:
#         if web_browser_type == "chrome":
#             # 安裝 ChromeDriver（如果使用 Chrome 瀏覽器）
#             # chromedriver_autoinstaller.install()  # 自動安裝 ChromeDriver
#             chrome_options = webdriver.ChromeOptions()
#             prefs = {"download.default_directory": main_download_path}
#             chrome_options.add_experimental_option("prefs", prefs)
#             chrome_options.add_argument("--headless") # 無頭模式
#             chrome_options.add_argument("--no-sandbox") # 禁用沙盒安全模式
#             chrome_options.add_argument("--disable-dev-shm-usage") #禁用共享內存
#             chrome_options.add_argument("--disable-gpu") # 禁用 GPU 硬件加速
#             chrome_options.add_argument("--window-size=1920x1080") # 設定窗口大小
#             driver = webdriver.Chrome(options=chrome_options)

#         if web_browser_type == "edge":
#             # 使用 Edge 的 webdriver_manager 自動安裝 EdgeDriver
#             edge_options = webdriver.EdgeOptions()
#             edge_options.add_argument("--headless")
#             edge_options.add_argument("--no-sandbox")
#             edge_options.add_argument("--disable-dev-shm-usage")
#             edge_options.add_argument("--disable-gpu")
#             edge_options.add_argument("--window-size=1920x1080")
#             driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=edge_options)

#         elif web_browser_type == "firefox":
#             # 使用 Firefox 的 webdriver_manager 自動安裝 GeckoDriver
#             firefox_options = webdriver.FirefoxOptions()
#             firefox_options.add_argument("--headless")
#             driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)

#         elif web_browser_type == "safari":
#             # 使用 SafariDriver，無需安裝，僅限 Mac 使用
#             driver = SafariDriver()

#         elif web_browser_type == "opera":
#             # 使用 Opera 的 webdriver_manager 自動安裝 OperaDriver
#             opera_options = webdriver.ChromeOptions()
#             opera_options.add_argument("--headless")
#             driver = webdriver.Chrome(OperaDriverManager().install(), options=opera_options)

#         else:
#             raise ValueError("Unsupported browser type!")

#         # 打開目標 URL
#         driver.get(user_input_url)

#         # 點開 Study_Metadata_Files 資料夾
#         Study_Metadata_Files = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='cdk-accordion-child-8']/div/div/div/repo-files-panel/app-geode-tree/div/div/div[4]/span/div/span[2]/a/div/div[1]/div/span[2]/span[2]"))
#         )
#         Study_Metadata_Files.click()

#         # 抓取 zip 檔的檔名 (ex: OSD-379_metadata_OSD-379-ISA)
#         file_name_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='cdk-accordion-child-8']/div/div/div/repo-files-panel/app-geode-tree/div/div/div[4]/span/div/span[3]/a/div/div[1]/div/span[2]/span[2]"))
#         )
#         file_name = file_name_element.text[:-4]  # 獲取檔名文本

#         # 建立 dataset_folder 的路徑
#         dataset_folder = os.path.join(extract_files_path, file_name)

#         # 如果 dataset_folder 資料夾已存在，刪除並重新創建
#         if os.path.exists(dataset_folder):
#             shutil.rmtree(dataset_folder)

#         # 創建新的 dataset_folder 資料夾
#         os.makedirs(dataset_folder)

#         # 自動掃描 dataset_folder 以檢查壓縮檔是否存在
#         zip_file_name = file_name_element.text
#         zip_file_path = os.path.join(main_download_path, zip_file_name)

#         # 如果檔案存在，則刪除
#         if os.path.exists(zip_file_path):
#             os.remove(zip_file_path)

#         # 模擬勾選 checkbox
#         checkbox = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='cdk-accordion-child-8']/div/div/div/repo-files-panel/app-geode-tree/div/div/div[4]/span/div/span[2]/a/div/div[1]/div/span[1]/span/input"))
#         )
#         checkbox.click()

#         # 模擬點擊下載按鈕
#         download_button = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='cdk-accordion-child-8']/div/div/div/repo-files-panel/app-geode-tree/div/div/div[2]/div/button/span[1]"))
#         )
#         download_button.click()

#         # 等待文件下載完成
#         timeout = 60  # 設定超時時間
#         start_time = time.time()
#         while not os.path.exists(zip_file_path):
#             if time.time() - start_time > timeout:
#                 raise ValueError("Operation timed out, the file was not found for download!")
#             time.sleep(1)  # 每隔一秒檢查一次

#         # 如果找到文件，執行解壓縮操作
#         if os.path.exists(zip_file_path):
#             with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#                 zip_ref.extractall(dataset_folder)  # 解壓縮到指定路徑

#         driver.quit()

#     except Exception as e:
#         # 捕捉並拋出錯誤
#         raise ValueError(f"Error: {str(e)}")