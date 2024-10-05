import os
from dash import html

# 設定資料夾路徑
DATA_FOLDER_PATH = './data'
DESKTOP_FOLDER_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "NASA_OSDR_Downloads")

# 掃描指定資料夾，提取檔案的編號（例如：OSD-379）
# param folder_path: 要掃描的資料夾路徑
# return: 檔案名稱的編號列表
def get_experiment_files_app(folder_path):
        if os.path.exists(folder_path):
             # 列出資料夾中的所有子資料夾
             directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
             experiment_files = []
        
             for directory in directories:
                 # 檢查資料夾名是否包含 "_"
                 if "_" in directory:
                     # 提取資料夾名中的前半部分（如 "OSD-379"）
                     experiment_files.append(directory.split('_')[0])
                #  else:
                #      print(f"警告：資料夾 '{directory}' 格式不正確，預期應包含 '_'.")
        
             return experiment_files
        else:
            return []  # 如果資料夾不存在，返回空列表
        
def get_osd_379_images():
     # OSD-379 URL處理邏輯
     osd_379_background_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-379/Experiment-Background.png?raw=true"
     osd_379_process_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-379/Experiment-Process.png?raw=true"
     osd_379_results_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-379/Experiment-Results.png?raw=true"
     
     return [
          html.Img(src=osd_379_background_image_url, style={'width': '100%', 'height': 'auto'}),  # Background區塊顯示圖片
          html.Img(src=osd_379_process_image_url, style={'width': '100%', 'height': 'auto'}),  # Process區塊顯示圖片
          html.Img(src=osd_379_results_image_url, style={'width': '100%', 'height': 'auto'})  # Results區塊顯示圖片
     ]

def get_osd_665_images():
     # OSD-665 URL處理邏輯
     osd_665_background_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-665/Experiment-Background.png?raw=true"
     osd_665_process_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-665/Experiment-Process.png?raw=true"
     osd_665_results_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-665/Experiment-Results.png?raw=true"
     
     return [
          html.Img(src=osd_665_background_image_url, style={'width': '100%', 'height': 'auto'}),  # Background區塊顯示圖片
          html.Img(src=osd_665_process_image_url, style={'width': '100%', 'height': 'auto'}),  # Process區塊顯示圖片
          html.Img(src=osd_665_results_image_url, style={'width': '100%', 'height': 'auto'})  # Results區塊顯示圖片
     ]
     
def get_compare_images():
     # Compare URL處理邏輯
     compare_background_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/Compare/Experiment-Background.png?raw=true"
     compare_process_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/Compare/Experiment-Process.png?raw=true"
     compare_results_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/Compare/Experiment-Results.png?raw=true"
     
     return [
          html.Img(src=compare_background_image_url, style={'width': '100%', 'height': 'auto'}),  # Background區塊顯示圖片
          html.Img(src=compare_process_image_url, style={'width': '100%', 'height': 'auto'}),  # Process區塊顯示圖片
          html.Img(src=compare_results_image_url, style={'width': '100%', 'height': 'auto'})  # Results區塊顯示圖片
     ]
