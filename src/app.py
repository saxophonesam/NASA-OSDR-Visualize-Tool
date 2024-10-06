import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html
from dash import dcc
import dash_daq as daq
import dash_bootstrap_components as dbc  # 如果需要 Bootstrap 樣式，可以安裝使用
import time

from layout_helper import run_standalone_app
# from load_data_from_nasa_osdr import load_data_from_nasa_osdr_app
from analyze_data import get_experiment_files_app, DATA_FOLDER_PATH, DESKTOP_FOLDER_PATH
from analyze_data import get_osd_379_images,get_osd_665_images,get_compare_images

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
                                # RadioItems
                                html.Div([
                                    dcc.RadioItems(
                                        id='link-repository-radio-options',
                                        options=[
                                            {'label': 'OSD-379', 'value': 'osd-379'},
                                            {'label': 'OSD-665', 'value': 'osd-665'},
                                            {'label': 'Enter link', 'value': 'enter-link'}
                                        ],
                                        value='osd-379',  # 預設選擇第一個選項
                                        className='radio-options'
                                    ),
                                ],style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '15px'}),

                                # Link輸入框和visualize按鈕
                                html.Div([
                                    dcc.Input(placeholder="Enter repository link...", type="text", id="user-input-url", className="link-repository-input"),
                                ], style={'text-align': 'center', 'margin-bottom': '10px'}),

                                html.Div([
                                    html.Button("Visualize", id="visualize-button", className="link-repository-button"),
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

                                # # Description顯示
                                html.Div([
                                    html.P(["Description :",html.Br(),
                                            """
                                            Choose OSD-379 or OSD-665 to quickly preview the visualization results,
                                            or enter the database link you're interested in
                                            and wait patiently for the visualization results.
                                            """
                                    ], className="link-repository-description")
                                ])
                            ], className="custom-box-content")
                        ], style=generate_custom_box_style(100, '0.85')),

                        # Experiments Compare區塊
                        html.Div([
                            html.Div("Experiments Compare", className="custom-box-header"),
                            html.Div([
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

                                html.Div([
                                    # html.Button("List all", id='list-all-button', className="link-repository-button"),
                                    html.Button("Compare", id='compare-button', className="link-repository-button"),
                                ], style={'text-align': 'center', 'margin-top': '15px'}),  # 按鈕區域

                                
                            ], className="custom-box-content")
                        ], style=generate_custom_box_style(100, '1.8'))

                    ], className="content-left-side"), #佔網頁寬度比例1/3 + 分隔線

                    # Content右半邊(由上到下排列的三個區塊)
                    html.Div([
                        html.Div([
                            html.Div("Experiment Visualization", className="custom-box-header"),
                            dcc.Tabs(id="tabs-description", value='tab-1', children=[
                                # Experiment Description區塊
                                dcc.Tab(label='Experiments Description', value='tab-1', children=[
                                    dcc.Loading(id="loading-description", children=[
                                        html.Div("Description information will be shown here.", id="exp-description", className="custom-box-content"),
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
            Output("link-repository-status-indicator", "children"), # 更新link repository status指示器
            Output("experiments-compare-status-indicator", "children"), # 更新compare status指示器
            Output("exp-description", "children"), # 更新Description區塊
            Output("exp-process", "children"), # 更新process區塊
            Output("exp-results", "children"), # 更新results區塊
        ],

        [   # 監聽不同按鈕的點擊
            Input("link-repository-radio-options", "value"),  # 監聽 radio button 的選擇變化
            Input("visualize-button", "n_clicks"),
            Input("compare-button", "n_clicks")
        ], 
        [
            State("user-input-url", "value") # 讀取輸入框值
        ]
    )
    def load_and_visualize(radio_options_value, visualize_clicks, compare_clicks, user_input_url):
        # 取得當前觸發回調的上下文
        ctx = dash.callback_context

        # 如果按鈕沒有被點擊
        if not ctx.triggered:
            raise PreventUpdate
        
        # 獲取觸發回調的按鈕ID
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # 如果是 Upload Data 按鈕被點擊
        if button_id == "visualize-button":
            # 如果在有輸入連結的情況下按下了visualize按鈕並且Radio Button的值為 'osd-379' 或 'osd-665'便禁止操作
            if radio_options_value == 'osd-379' and not user_input_url:
                time.sleep(2)

                # 這裡加入OSD-379圖片的URL，並使用html.Img顯示           
                images = get_osd_379_images()
                OSD_379_description, OSD_379_process, OSD_379_results = images

                return (
                    "Visualization of OSD-379 is completed!",  # link repository Status
                    "Visualization of OSD-379 is stored!",  # compare Status
                    OSD_379_description, # description區塊
                    OSD_379_process, # Process區塊
                    OSD_379_results # Results區塊
                )
            elif radio_options_value == 'osd-665' and not user_input_url:
                time.sleep(2)

                # 這裡加入OSD-665圖片的URL，並使用html.Img顯示           
                images = get_osd_665_images()
                OSD_665_description, OSD_665_process, OSD_665_results = images

                return (
                    "Visualization of OSD-665 is completed!",  # link repository Status
                    "Visualization of OSD-665 is stored!",  # compare Status
                    OSD_665_description, # description區塊
                    OSD_665_process, # Process區塊
                    OSD_665_results # Results區塊
                )
            elif radio_options_value in ['osd-379', 'osd-665'] and user_input_url:
                return (
                    "Operation not allowed!",  # link repository Status
                    "No updates.",  # compare Status
                    "No updates.",  # description區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            elif radio_options_value == 'enter-link' and not user_input_url:
                return (
                    "No URL provided, cannot proceed!",  # link repository Status
                    "No updates.",  # compare Status
                    "No updates.",  # description區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            elif user_input_url and radio_options_value == 'enter-link':
                try:
                    # 如果 quick view 開關是 OFF，且輸入框有輸入值，則將輸入的值賦給 user_input_url
                    # web_browser_type = "edge"
                    # load_data_from_nasa_osdr_app(user_input_url, web_browser_type)

                    time.sleep(2)

                    if user_input_url == "https://osdr.nasa.gov/bio/repo/data/studies/OSD-379":
                        # # OSD-379 URL處理邏輯                        
                        images = get_osd_379_images()
                        OSD_379_description, OSD_379_process, OSD_379_results = images

                        return (
                            "Visualization of OSD-379 is completed!",  # link repository Status
                            "Visualization of OSD-379 is stored!",  # compare Status
                            OSD_379_description,  # description區塊
                            OSD_379_process,     # Process區塊
                            OSD_379_results      # Results區塊
                        )

                    elif user_input_url == "https://osdr.nasa.gov/bio/repo/data/studies/OSD-665":
                        # OSD-665 URL處理邏輯                   
                        images = get_osd_665_images()
                        OSD_665_description, OSD_665_process, OSD_665_results = images

                        return (
                            "Visualization of OSD-665 is completed!",  # link repository Status
                            "Visualization of OSD-665 is stored!",  # compare Status
                            OSD_665_description,  # description區塊
                            OSD_665_process,     # Process區塊
                            OSD_665_results      # Results區塊
                        )

                    else:
                        return (
                            f"Invalid URL: {user_input_url}",  # 顯示錯誤訊息在 link repository Status
                            "No updates.",  # compare Status
                            "No updates.",  # description區塊
                            "No updates.",  # Process區塊
                            "No updates."  # Results區塊
                        )
                    
                except ValueError as e:
                    # 捕捉 ValueError 並將錯誤訊息顯示到頁面
                    return (
                        f"Error: {str(e)}",  # 顯示錯誤訊息在 link repository Status
                        "No updates.",  # compare Status
                        "No updates.",  # description區塊
                        "No updates.",  # Process區塊
                        "No updates."  # Results區塊
                    )
            else:
                return (
                    "Operation not allowed!",  # link repository Status
                    "No updates.",  # compare Status
                    "No updates.",  # description區塊
                    "No updates.",  # Process區塊
                    "No updates."  # Results區塊
                )
            
        # 如果是 Upload Data 按鈕被點擊
        if button_id == "compare-button":
            time.sleep(2)
            # 這裡加入OSD-665圖片的URL，並使用html.Img顯示           
            images = get_compare_images()
            Compare_description, Compare_process, Compare_results = images

            return (
                "",  # link repository Status
                "Experiments compared successfully!",  # compare Status
                Compare_description, # description區塊
                Compare_process, # Process區塊
                Compare_results # Results區塊
            )
            
        raise PreventUpdate


app = run_standalone_app(layout, callbacks, header_colors)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)            #上傳時用
    # app.run_server(debug=True, port=8051) #Debug時用
