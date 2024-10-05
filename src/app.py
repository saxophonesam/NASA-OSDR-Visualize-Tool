import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html
from dash import dcc
import dash_daq as daq
import time

from layout_helper import run_standalone_app
# from load_data_from_nasa_osdr import load_data_from_nasa_osdr_app
from analyze_data import get_experiment_files_app, DATA_FOLDER_PATH, DESKTOP_FOLDER_PATH

# 定義動態生成樣式的函數
def generate_custom_box_style(width, aspect_ratio):
    return {
        'background-color': '#f5f5f5',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'padding': '0',
        'margin': '10px',
        'width': f'{width}%',  # 動態設定寬度
        'height': 'auto',  # 高度自動
        'aspect-ratio': aspect_ratio,  # 使用寬高比，讓高度隨寬度變化
        'overflow': 'hidden',
        'display': 'inline-block',
        'vertical-align': 'top'
    }

def generate_custom_box_style_px(width, height):
    return {
        'background-color': '#f5f5f5',
        'border': '1px solid #ccc',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'padding': '0',
        'margin': '10px',
        'width': f'{width}%',  # 動態設定寬度
        'height': f'{height}px',  # 動態高度自動
        'overflow': 'hidden',
        'display': 'inline-block',
        'vertical-align': 'top'
    }

def header_colors():
    return {
        'bg_color': '#2F2F2F',
        'font_color': 'white'
    }


def layout():
    return html.Div(
        id='NASA-OSDR-Visualize-Tool-body',
        className='app-body',
        children=[
            # Content 網頁中間內容滾動區域
            html.Div([
                html.Div([
                    # Content左半邊(上下兩個區塊)
                    html.Div([
                        # Link Repository區塊
                        html.Div([
                            html.Div("Link Repository", className="custom-box-header"),
                            html.Div([
                                # Quick View 開關
                                html.Div([
                                    html.P("Quick view : ", className="link-repository-font"),
                                    daq.BooleanSwitch(id="quick-view-switch", color="#2922ff", on=True),
                                ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '15px'}),
                                
                                # OSD Buttons
                                html.Div([
                                    html.Button("OSD-379", id="osd-379", className="link-repository-button"),
                                    html.Button("OSD-665", id="osd-665", className="link-repository-button"),
                                ], style={'text-align': 'center', 'margin-bottom': '15px'}),

                                # Link輸入框和Upload按鈕
                                html.Div([
                                    dcc.Input(placeholder="Enter repository link...", type="text", id="user-input-url", className="link-repository-input"),
                                ], style={'text-align': 'center', 'margin-bottom': '10px'}),

                                html.Div([
                                    html.Button("Upload Data", id="upload-data", className="link-repository-button"),
                                ], style={'text-align': 'center'}),

                                # Status 顯示
                                html.Div([
                                    html.P("Status: ", className="link-repository-font", style={'display': 'inline-block', 'margin-right': '10px'}),  # Status 文字
                                    dcc.Loading(  # 使用Loading包裹狀態顯示
                                        id="link-repository-loading-status",
                                        children=[
                                            html.Div(id="link-repository-status-indicator", className="link-repository-font", style={'display': 'inline-block'})
                                        ],
                                        type="default",
                                    )
                                ], style={'text-align': 'center', 'margin-top': '10px', 'margin-bottom': '15px'}),

                                # Description顯示
                                html.Div([
                                    html.P(["Description :",html.Br(),
                                            """
                                            Please enter the database link you're interested in
                                            and wait patiently for the visualization results.
                                            The metadata will be downloaded to your desktop simultaneously.
                                            """
                                    ], className="link-repository-description")
                                ])
                            ], className="custom-box-content")
                        ], style=generate_custom_box_style(100, '0.85')),

                        # Experiments Compare區塊
                        html.Div([
                            html.Div("Experiments Compare", className="custom-box-header"),
                            html.Div([
                                # Memory Selection (下拉選單)
                                dcc.Dropdown(
                                    id='memory-selection',
                                    options=[],  # 初始為空，待觸發後更新
                                    multi=True,
                                    value=[],  # 預設選擇的項目
                                    placeholder="Select experiments...",  # 提示文字
                                ),
                                # List all 和 Compare 按鈕
                                html.Div([
                                    html.Button("List all", id='list-all-button', className="link-repository-button"),
                                    html.Button("Compare", id='compare-button', className="link-repository-button"),
                                ], style={'text-align': 'center', 'margin-top': '15px'}),  # 按鈕區域

                                # Status 顯示
                                html.Div([
                                    html.P("Status: ", className="link-repository-font", style={'display': 'inline-block', 'margin-right': '10px'}),  # Status 文字
                                    dcc.Loading(  # 使用Loading包裹狀態顯示
                                        id="experiments-compare-loading-status",
                                        children=[
                                            html.Div(id="experiments-compare-status-indicator", className="link-repository-font", style={'display': 'inline-block'})
                                        ],
                                        type="default",
                                    )
                                ], style={'text-align': 'center', 'margin-top': '10px', 'margin-bottom': '15px'}),
                            ], className="custom-box-content")
                        ], style=generate_custom_box_style(100, '1.8'))

                    ], className="content-left-side"), #佔網頁寬度比例1/3 + 分隔線

                    # Content右半邊(由上到下排列的三個區塊)
                    html.Div([
                        html.Div([
                            html.Div("Experiment Visualization", className="custom-box-header"),
                            dcc.Tabs(id="tabs-background", value='tab-1', children=[
                                # Experiment Background區塊
                                dcc.Tab(label='Experiments Background', value='tab-1', children=[
                                    dcc.Loading(id="loading-background", children=[
                                        html.Div("Background information will be shown here.", id="exp-background", className="custom-box-content"),
                                    ]),
                                ]),

                                # Experiment Process區塊
                                dcc.Tab(label='Experiment Process', value='tab-2', children=[
                                    dcc.Loading(id="loading-process", children=[
                                        html.Div("Process data will be shown here.", id="exp-process", className="custom-box-content"),
                                    ]),
                                ]),

                                # Experiment Results區塊
                                dcc.Tab(label='Experiment Results', value='tab-3', children=[
                                    dcc.Loading(id="loading-results", children=[
                                        html.Div("Data Results will be shown here.", id="exp-results", className="custom-box-content"),
                                    ]),
                                ]),
                            ]),
                         ], style=generate_custom_box_style(100, '1.4')),
                    ], className="content-right-side") #佔網頁寬度比例2/3
                ], style={'display': 'flex', 'justify-content': 'space-between'}),
            ], id="app-content"),

        ]
    )


def callbacks(_app):
    @_app.callback(
        [
            Output("link-repository-status-indicator", "children"), # 更新status指示器
            Output("exp-background", "children"), # 更新background區塊
            Output("exp-process", "children"), # 更新process區塊
            Output("exp-results", "children"), # 更新results區塊
        ],

        [   # 監聽不同按鈕的點擊
            Input("osd-379", "n_clicks"), 
            Input("osd-665", "n_clicks"),
            Input("upload-data", "n_clicks")
        ], 
        [
            State("quick-view-switch", "on"), # 確認quick-view開關狀態
            State("user-input-url", "value") # 讀取輸入框值
        ]
    )
    def load_and_visualize(osd_379_clicks, osd_665_clicks, upload_data_clicks, quick_view_enabled, user_input_url):
        # 取得當前觸發回調的上下文
        ctx = dash.callback_context

        # 如果按鈕沒有被點擊
        if not ctx.triggered:
            raise PreventUpdate
        
        # 獲取觸發回調的按鈕ID
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # 如果是 Upload Data 按鈕被點擊
        if button_id == "upload-data":
            # Quick View 開啟時禁止操作
            if quick_view_enabled and user_input_url:
                return (
                    "Quick view is enabled, operation not allowed!",  # Status
                    "Quick view is enabled, no updates.",  # Background區塊
                    "Quick view is enabled, no updates.",  # Process區塊
                    "Quick view is enabled, no updates."  # Results區塊
                )
            elif user_input_url:
                try:
                    # 如果 quick view 開關是 OFF，且輸入框有輸入值，則將輸入的值賦給 user_input_url
                    time.sleep(3)  # 模擬 3 秒的處理
                    # web_browser_type = "edge"
                    # load_data_from_nasa_osdr_app(user_input_url, web_browser_type)

                    # 成功後更新頁面狀態
                    return (
                        "Data successfully downloaded and processed!",  # Status
                        "Experiments Background updated.",  # Background區塊
                        "Experiments Process updated.",  # Process區塊
                        "Experiments Results updated."  # Results區塊
                    )
                except ValueError as e:
                    # 捕捉 ValueError 並將錯誤訊息顯示到頁面
                    return (
                        f"Error: {str(e)}",  # 顯示錯誤訊息在 Status
                        "No updates.",  # Background區塊
                        "No updates.",  # Process區塊
                        "No updates."  # Results區塊
                    )
            elif quick_view_enabled and not user_input_url:
                return (
                    "Quick view is enabled, operation not allowed!",  # Status
                    "No updates.",  # Background區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            else:
                return (
                    "No URL provided, cannot proceed!",  # Status
                    "No updates.",  # Background區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            
        # 如果按的是 OSD-379 按鈕
        if button_id == "osd-379":
            if quick_view_enabled:
                time.sleep(2)

                # 這裡加入OSD-379圖片的URL，並使用html.Img顯示
                osd_379_background_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-379/Experiment-Background.png?raw=true"
                OSD_379_background=html.Img(src=osd_379_background_image_url, style={'width': '100%','height': '100',}), # Background區塊顯示圖片

                osd_379_process_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-379/Experiment-Process.png?raw=true"
                OSD_379_process=html.Img(src=osd_379_process_image_url, style={'width': '100%','height': '100',}), # Process區塊顯示圖片

                osd_379_results_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-379/Experiment-Results.png?raw=true"
                OSD_379_results=html.Img(src=osd_379_results_image_url, style={'width': '100%','height': '100',}), # Results區塊顯示圖片

                return (
                    "Visualization of OSD-379 is completed!",  # Status
                    OSD_379_background, # Background區塊
                    OSD_379_process, # Process區塊
                    OSD_379_results # Results區塊
                )
            else:
                return (
                    "Quick view is disabled, operation not allowed!",  # Status
                    "No updates.",  # Background區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            
        # 如果按的是 OSD-665 按鈕
        if button_id == "osd-665":
            if quick_view_enabled:
                time.sleep(2)

                # 這裡加入OSD-379圖片的URL，並使用html.Img顯示
                osd_665_background_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-665/Experiment-Background.png?raw=true"
                OSD_665_background=html.Img(src=osd_665_background_image_url, style={'width': '100%','height': '100',}), # Background區塊顯示圖片

                osd_665_process_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-665/Experiment-Process.png?raw=true"
                OSD_665_process=html.Img(src=osd_665_process_image_url, style={'width': '100%','height': '100',}), # Process區塊顯示圖片

                osd_665_results_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/OSD-665/Experiment-Results.png?raw=true"
                OSD_665_results=html.Img(src=osd_665_results_image_url, style={'width': '100%','height': '100',}), # Results區塊顯示圖片

                return (
                    "Visualization of OSD-665 is completed!",  # Status
                    OSD_665_background, # Background區塊
                    OSD_665_process, # Process區塊
                    OSD_665_results # Results區塊
                )
            else:
                return (
                    "Quick view is disabled, operation not allowed!",  # Status
                    "No updates.",  # Background區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            
    @_app.callback(
        [
            Output('memory-selection', 'options'), # 更新下拉選單的選項
            Output('memory-selection', 'value'), # 更新下拉選單的選擇值
            Output("experiments-compare-status-indicator", "children") # 更新status指示器
        ],
        Input('list-all-button', 'n_clicks'),
        State("quick-view-switch", "on"),
    )
    def list_all_experiments(n_clicks, quick_view_value):
        # 取得當前觸發回調的上下文
        ctx = dash.callback_context

        # 如果按鈕沒有被點擊
        if not ctx.triggered:
            raise PreventUpdate
    
        # 獲取觸發回調的按鈕ID
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # 檢查是否是 list all 按鈕被點擊
        if button_id == 'list-all-button':
            # 根據 Quick View 狀態，決定訪問的資料夾
            if quick_view_value:
                # experiment_files = get_experiment_files_app(DATA_FOLDER_PATH)
                experiment_files = ['OSD-379','OSD-665']
            else:
                # experiment_files = get_experiment_files_app(DESKTOP_FOLDER_PATH)
                experiment_files = []

            # 判斷是否有檔案存在
            if not experiment_files:
                return [], [], "No files! Please go to Link Repository and upload data first"

            # 構建下拉選單的 options
            # options = [{'label': f"{file}", 'value': file} for file in experiment_files]
            options = [{'label': file, 'value': file} for file in experiment_files]

            # 回傳 options 和 value 以及 status 訊息
            # return options, [file for file in experiment_files], "Operation completed!"
            return options, experiment_files, "Operation completed!"
    
        raise PreventUpdate  # 如果不是 list all 按鈕，則不進行更新
    
    @_app.callback(
    [
        Output("exp-background", "children", allow_duplicate=True),  # 更新 background 區塊
        Output("exp-process", "children", allow_duplicate=True),     # 更新 process 區塊
        Output("exp-results", "children", allow_duplicate=True),     # 更新 results 區塊
        Output("experiments-compare-status-indicator", "children", allow_duplicate=True),  # 更新 status 區塊
    ],
    Input("compare-button", "n_clicks"),   # 監聽 Compare 按鈕
    State("memory-selection", "value"),    # 監聽 Dropdown 的選擇狀態
    prevent_initial_call=True  # 禁止在初次加載時觸發回調
    )
    def compare_experiments(compare_clicks, selected_experiments):
        # 取得當前觸發回調的上下文
        ctx = dash.callback_context

        # 如果按鈕沒有被點擊，則不進行更新
        if not ctx.triggered:
            raise PreventUpdate

        # 獲取觸發回調的按鈕ID
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # 檢查是否是 Compare 按鈕被點擊
        if button_id == "compare-button":
            # 檢查是否選擇了兩個或更多的實驗
            if len(selected_experiments) < 2:
                return (
                    "No updates.",  # 更新 background 區塊
                    "No updates.",  # 更新 process 區塊
                    "No updates.",  # 更新 results 區塊
                    "Please select at least two experiments."  # Status
                )
            
            time.sleep(2)
            
            # 這裡加入Compare圖片的URL，並使用html.Img顯示
            compare_background_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/Compare/Experiment-Background.png?raw=true"
            Compare_background=html.Img(src=compare_background_image_url, style={'width': '100%','height': '100',}), # Background區塊顯示圖片

            compare_process_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/Compare/Experiment-Process.png?raw=true"
            Compare_process=html.Img(src=compare_process_image_url, style={'width': '100%','height': '100',}), # Process區塊顯示圖片

            compare_results_image_url = "https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/blob/main/image/Compare/Experiment-Results.png?raw=true"
            Compare_results=html.Img(src=compare_results_image_url, style={'width': '100%','height': '100',}), # Results區塊顯示圖片

            return (
                Compare_background, # Background區塊
                Compare_process, # Process區塊
                Compare_results, # Results區塊
                "Experiments compared successfully!"  # Status 
            )
        
        raise PreventUpdate  # 如果不是預期的按鈕被點擊，則不更新


app = run_standalone_app(layout, callbacks, header_colors)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)            #上傳時用
    # app.run_server(debug=True, port=8051) #Debug時用
