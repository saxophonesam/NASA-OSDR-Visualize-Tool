import os

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
