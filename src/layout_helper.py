import os
import base64
import dash
from dash import dcc 
from dash import html

def run_standalone_app(
        layout,
        callbacks,
        header_colors,
):
    app = dash.Dash(__name__)
    app.scripts.config.serve_locally = True
    # Handle callback to component with id "fullband-switch"
    app.config['suppress_callback_exceptions'] = True

    app_title = "NASA OSDR Visualize App"

    # Assign layout
    app.layout = app_page_layout(
        page_layout=layout(),
        app_title=app_title,
        **header_colors()
    )

    # Register all callbacks
    callbacks(app)

    # return app object
    return app

def app_page_layout(page_layout,
                    app_title="NASA OSDR Visualize App",
                    light_logo=True,
                    bg_color="#506784",
                    font_color="#F3F6FA"):
    
      # 獲取當前.py文件的目錄
    current_directory = os.path.dirname(__file__)
    nasa_logo_path = os.path.join(current_directory, 'assets/nasa-logo.png')
    github_logo_path = os.path.join(current_directory, 'assets/GitHub-Mark-{}64px.png'.format(
        'Light-' if light_logo else ''))
    
    # 打開 nasa logo 並進行 base64 編碼
    with open(nasa_logo_path, 'rb') as image_file:
        nasa_logo_base64 = base64.b64encode(image_file.read()).decode()

    # 打開 GitHub logo 並進行 base64 編碼
    with open(github_logo_path, 'rb') as image_file:
        github_logo_base64 = base64.b64encode(image_file.read()).decode()

    return html.Div(
        id='main_page',
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                id='app-page-header',
                children=[
                    html.A(
                        id='nasa-logo', children=[
                            html.Img(
                                src=f'data:image/png;base64,{nasa_logo_base64}'
                            )
                        ],
                        href="https://osdr.nasa.gov/bio/repo/search?q=&data_source=cgene,alsda&data_type=study",
                        target="_blank"  # 在新分頁中打開
                    ),
                    html.H2(
                        app_title
                    ),

                    html.A(
                        id='gh-link',
                        children=[
                            'View on GitHub'
                        ],
                        href="https://github.com/saxophonesam/NASA-OSDR-Visualize-Tool/tree/main",
                        target="_blank",  # 在新分頁中打開
                        style={'color': 'white' if light_logo else 'black',
                               'border': 'solid 1px white' if light_logo else 'solid 1px black'}
                    ),

                    html.Img(
                        src=f'data:image/png;base64,{github_logo_base64}'
                    )
                ],
                style={
                    'background': bg_color,
                    'color': font_color,
                }
            ),
            html.Div(
                id='app-page-content',
                children=[
                    page_layout,  # Content 部分，從app.py中調用layout()來寫入
                    
                    # Footer 部分，使其接續在Content後呈現
                    html.Div(
                        id='app-footer',
                        children=[
                            html.P("© 2024 NASA Space Apps Challenge")
                        ]
                    )
                ]

            )

        ],
    )
