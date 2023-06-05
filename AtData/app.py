import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import dash_daq as daq
import datetime
from datetime import timedelta
import os
from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from dash_bootstrap_components._components.Container import Container
from dash_bootstrap_templates import ThemeSwitchAIO
import re

import app_func as func

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css], suppress_callback_exceptions=True)

#==================================================================================================================================
#========================================================  Components  ============================================================
#==================================================================================================================================

# Dropdown=========================================================================================================================
dropdown1 = dbc.DropdownMenu(
    label="Menu",
    size='lg',
    menu_variant="dark",
    children=[
        # dcc.Location(id='location1'),
        dcc.Link(
            dbc.DropdownMenuItem("New Acquisition"), href='/new_acquisition', id='link1', className='link'
        ),
        dbc.DropdownMenuItem("Update"),
        dbc.DropdownMenuItem("Problem Analysis"),
        dbc.DropdownMenuItem("Help & Support"),
    ], className='menu'
)
dropdown2 = dbc.DropdownMenu(
    label="Theme",
    size='lg',
    menu_variant="dark",
    #color='dark',
    children=[
        dbc.DropdownMenuItem("dark"),
        dbc.DropdownMenuItem("cosmo"),
        dbc.DropdownMenuItem("cyborg"),
    ], className='menu menu-theme'
)

# ThemeSwitch======================================================================================================================
theme_switch = ThemeSwitchAIO(
    aio_id="theme", themes=[dbc.themes.BOOTSTRAP, dbc.themes.QUARTZ]
)

# Header===========================================================================================================================
header = html.Div([
        html.Div([
            html.Img(src='assets/img/my-logo4.png', className='logo head'),
            html.P(
                "AtData", className="text-white title1 head"),
            html.P(
                "~データで見るAtCoder~", className="text-white title2 head"),

    ],className='head1'),
       
    html.Div([ 
    dcc.Location(id='location1'),
    dbc.NavItem(dbc.NavLink("Home", href="/home", className='text-white home')),
    dropdown1,
    dropdown2,
    theme_switch
    ], className='head2')
        
],className='bg-primary header'
)

# Settings=========================================================================================================================
settings = dbc.Form(
    dbc.Row(
        [
            dbc.Col(
                dbc.InputGroup(
                    [dbc.InputGroupText("You:", className='setting-item'), 
                     dbc.Input(placeholder="Enter UserID(半角)", className='setting-item', id='input_you', persistence=True)],
                    className="mb-3",
                ),
            ),
            dbc.Col(
                dbc.InputGroup(
                    [dbc.InputGroupText("Rival:", className='setting-item'), 
                     dbc.Input(placeholder="Enter UserID(半角)", className='setting-item', id='input_rival', persistence=True)],
                    className="mb-3",
                ),
            ),
            dbc.Col(dbc.Button("Apply", color="primary", className='apply setting-item', id='button_apply')),
        ],
        # className="g-2",
    ), className='settings'
)

first_card = dbc.Spinner(dbc.Card(
    dbc.CardBody(
        [
            html.H5("Max-Streaks: -Days", className="card-title", id='max_streaks'),
            html.H5("Now-Streaks: -Days", className="card-title", id='now_streaks'),
            html.H5("Submissions-Yesterday: 0Submissions", className="card-title", id='sub_y'),
            # html.P("This card has some text content, but not much else"),
            # dbc.Button("Go somewhere", color="primary"),
        ]
    ), className='cards', id='card_streak'
), color='light')
second_card = dbc.Spinner(dbc.Card(
    dbc.CardBody(
        [
            html.H5("Max-Streaks: -Days", className="card-title", id='max_streaks_r'),
            html.H5("Now-Streaks: -Days", className="card-title", id='now_streaks_r'),
            html.H5("Submissions-Yesterday: -Submissions", className="card-title", id='sub_y_r'),
            # html.P("This card has some text content, but not much else"),
            # dbc.Button("Go somewhere", color="primary"),
        ]
    ), className='cards'
), color='light')
third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Rating: -", className="rating_you", id='rating_you'),
            html.H5("Highest-Rating: -", className="h_rating_you", id='h_rating_you'),
            html.H5("Highest-Performance: -", className="h_performance_you", id='h_performance_you'),
            # html.P("This card has some text content, but not much else"),
            # dbc.Button("Go somewhere", color="primary"),
        ]
    ), className='cards'
)
fourth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Rating: -", className="rating_rival", id='rating_rival'),
            html.H5("Highest-Rating: -", className="h_rating_rival", id='h_rating_rival'),
            html.H5("Highest-Performance: -", className="h_performance_rival", id='h_performance_rival'),
            # html.P("This card has some text content, but not much else"),
            # dbc.Button("Go somewhere", color="primary"),
        ]
    ), className='cards'
)

cards = dbc.Row(
    [
        dbc.Col(first_card, width=6),
        dbc.Col(second_card, width=6),
    ], className='mt-3'
)
cards2 = dbc.Row(
    [
        dbc.Col(third_card, width=6),
        dbc.Col(fourth_card, width=6),
    ], className='mt-3'
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("日別の提出状況 (AtCoder Beginner Contest)", className="card-text text-white fs-4 fw-bolder"),
            html.Div([
                dbc.Spinner(dcc.Graph(className='tab1-fig', id='tab1_fig1', config={'displaylogo': False}), color='light'),
                dbc.Spinner(dcc.Graph(className='tab1-fig', id='tab1_fig2', config={'displaylogo': False}), color='light'),
            ], className='tab1-fig-contena'),
            cards
            # dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3 bg-primary",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("レーティングとパフォーマンス", className="card-text text-white fs-4 fw-bolder"),
            html.Div([
                dcc.Graph(className='tab1-fig', id='tab2_fig1'),
                dcc.Graph(className='tab1-fig', id='tab2_fig2'),
            ], className='tab1-fig-contena'),
            cards2
            # dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3 bg-primary",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("未実装です", className="card-text fw-bolder"),
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        []
    ),
    className="mt-3",
    id='battle_content'
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Everyday Achievement", active_tab_style={"font-weight": "bold", 'font-size': 20}),
        dbc.Tab(tab2_content, label="Contest Performance", active_tab_style={"font-weight": "bold", 'font-size': 20}),
        dbc.Tab(tab3_content, label="Submission Status", active_tab_style={"font-weight": "bold", 'font-size': 20}),
        dbc.Tab(tab4_content, label="Buttle", active_tab_style={"font-weight": "bold", 'font-size': 20}, id='tab4'),
        dbc.Tab(tab3_content, label="Error Analysis", active_tab_style={"font-weight": "bold", 'font-size': 20}),
        dbc.Tab(tab3_content, label="Diff Search", active_tab_style={"font-weight": "bold", 'font-size': 20}),
    ], className='tabs'
)

reg = html.Div([
    html.Div([
        html.H2(
            children='User ID',
            className='na_text',
        ),
        dbc.InputGroup(
            [dbc.Input(placeholder="Enter UserID(半角)", className='n', persistence=True, id='input_un')],
            size='lg',
            className="mb-3 na_input",
        ),

    ],style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '5%'}
    ),
    html.Div([
        html.H2(
            children='PassWord',
            className='na_text',
        ),
        dbc.InputGroup(
            [dbc.Input(placeholder="Enter PassWord(半角)", className='n', persistence=True, disabled=True)],
            size='lg',
            className="na_input",
        ),
    ],style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '0%'}
    ),
    html.P('※パスワード必須', style={'color': 'red', 'margin-bottom': '5%', 'margin-left': '34%'}),
    html.Div([
        dbc.Button("新規取得", color="primary", className='apply setting-item fw-bold', id='button_na', n_clicks=0,
                style={'width': '70%'}, outline=True),
    ],style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '2.5%'}),
    html.Div([
        dcc.Link(
        dbc.Button("ホームヘ戻る", color="secondary", className='apply setting-item fw-bold', id='button_apply', n_clicks=0,
                style={'width': '70%'}, outline=True),
        href='/home', style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}, className='link'),
        # style={'color': 'black', 'text-decoration': 'none',}),
    ],style={}),
    
    html.Div([html.H2('取得しました！！')],
    style={'text-align': 'center'}, id='new_div', className='mt-3')
],style={'width': '50%', 'margin-left': '25%', 'margin-top': '5%',\
    'padding': '3% 0', 'border': '5px solid #0d6cfc', 'border-radius': '8%',}
)

main = html.Div([
        settings,
        dbc.Row([
        dbc.Col(
        className='col-table', width=2, id='unsolve'),
        dbc.Col(
        tabs, className='col-tabs', width=10
        )], className='rr')

])

app.layout = dbc.Container(
    [
        header,
        html.Div([
        settings,
        dbc.Row([
        dbc.Col(
        className='col-table', width=2),
        dbc.Col(
        tabs, className='col-tabs', width=10
        )], className='rr')
        ],id='contents'),
    ],
    fluid=True,
    className="dbc",
)

#=================================================================================================================================
#========================================================CallBack=============================================================
#=================================================================================================================================

# Everyday Achievement
@app.callback(
    Output("tab1_fig1", "figure"),
    Output("tab1_fig2", "figure"),
    Output("max_streaks", "children"),
    Output("now_streaks", "children"),
    Output("sub_y", "children"),
    Output("max_streaks_r", "children"),
    Output("now_streaks_r", "children"),
    Output("sub_y_r", "children"),
    Input('button_apply', "n_clicks"),
    State('input_you', 'value'),
    State('input_rival', 'value')
)
def update_tab1(n_clicks, un_you, un_rival):
    if n_clicks==0:
        f = func.empty_fig('no_data')
        ms = 'Max-Streaks: -Days'
        ns = 'Now-Streaks: -Days'
        sy = 'Submissions-Yesterday: -Submissions'
        return f, f, ms, ns, sy, ms, ns, sy
    else:        
        # データが存在するかを確認(存在しない場合は，データが存在しませんと表示する)
        path = f'data/{un_you}/{un_you}.csv'
        path2 = f'data/{un_rival}/{un_rival}.csv'
        is_file = os.path.isfile(path)
        is_file2 = os.path.isfile(path2)               
        if is_file and is_file2:
            # you
            data = pd.read_csv(f'data/{un_you}/{un_you}.csv', index_col=0)
            data_date = data.sort_values('提出日時')
            fig_1 = func.make_fig1(data_date)
            ms_tmp, ns_tmp, sy_tmp = func.get_streaks(data_date)
            ms = f'Max-Streaks: {ms_tmp}Days'
            ns = f'Now-Streaks: {ns_tmp}Days'
            sy = f'Submissions-Yesterday: {sy_tmp}Sudbmissions'
            # rival
            data2 = pd.read_csv(f'data/{un_rival}/{un_rival}.csv', index_col=0)
            data_date2 = data2.sort_values('提出日時')
            fig_2 = func.make_fig1(data_date2)
            ms_tmp, ns_tmp, sy_tmp = func.get_streaks(data_date2)
            ms2 = f'Max-Streaks: {ms_tmp}Days'
            ns2 = f'Now-Streaks: {ns_tmp}Days'
            sy2 = f'Submissions-Yesterday: {sy_tmp}Submissions'

        
        # youのみデータが存在する場合
        elif is_file:
            data = pd.read_csv(f'data/{un_you}/{un_you}.csv', index_col=0)
            data_date = data.sort_values('提出日時')
            fig_1 = func.make_fig1(data_date)
            ms_tmp, ns_tmp, sy_tmp = func.get_streaks(data_date)
            ms = f'Max-Streaks: {ms_tmp}Days'
            ns = f'Now-Streaks: {ns_tmp}Days'
            sy = f'Submissions-Yesterday: {sy_tmp}Submissions'
            fig_2 = func.empty_fig('no_data')
            ms2 = 'Max-Streaks: -Days'
            ns2 = 'Now-Streaks: -Days'
            sy2 = 'Submissions-Yesterday: -Submissions'

        # rivalのみデータが存在する場合
        elif is_file2:
            data = pd.read_csv(f'data/{un_rival}/{un_rival}.csv', index_col=0)
            data_date = data.sort_values('提出日時')
            fig_2 = func.make_fig1(data_date)
            ms_tmp, ns_tmp, sy_tmp = func.get_streaks(data_date)
            ms2 = f'Max-Streaks: {ms_tmp}Days'
            ns2 = f'Now-Streaks: {ns_tmp}Days'
            sy2 = f'Submissions-Yesterday: {sy_tmp}Submissions'
            fig_1 = func.empty_fig('no_data')
            ms = 'Max-Streaks: -Days'
            ns = 'Now-Streaks: -Days'
            sy = 'Submissions-Yesterday: -Submissions'
                        
        else:
            fig_1 = func.empty_fig('データの取得を行なってください')
            ms = 'Max-Streaks: -Days'
            ns = 'Now-Streaks: -Days'
            sy = 'Submissions-Yesterday: -Submissions'
            fig_2 = func.empty_fig('データの取得を行なってください')
            ms2 = 'Max-Streaks: -Days'
            ns2 = 'Now-Streaks: -Days'
            sy2 = 'Submissions-Yesterday: -Submissions'
            
        return fig_1, fig_2, ms, ns, sy, ms2, ns2, sy2

    
# 新規取得
# @app.callback(
#     Output("new_div", "children"),
#     Input('button_na', "n_clicks"),
#     State('input_un', 'value'),
# )
# def get_data(n_clicks, un):
#     if n_clicks != 0:
#         g = func.Get(un)
#         exist = g.check_exist(un)  # ユーザーが存在するか確認
#         if exist:
#             os.mkdir(f'data/{un}')
#             df_submission = g.get_submission_data()
#             df_submission.to_csv(f'data/{un}/{un}.csv')
            
#             df_unsolve = g.get_unsolve(df_submission)
#             df_unsolve.to_csv(f'data/{un}/{un}_us.csv')
            
#             df_grade = g.make_df_grade(un)
#             df_grade.to_csv(f'data/{un}/{un}_grade.csv')
            
#             out = [html.H2('取得しました！！')]
#         else:
#             out = [html.H2('取得')]
            
#         return out
    
#     else:
#         out = html.H2('')
#         return out
        

#Contest Performance
@app.callback(
    Output("tab2_fig1", "figure"),
    Output("tab2_fig2", "figure"),
    Output("rating_you", "children"),
    Output("h_rating_you", "children"),
    Output("h_performance_you", "children"),
    Output("rating_rival", "children"),
    Output("h_rating_rival", "children"),
    Output("h_performance_rival", "children"),
    Input('button_apply', "n_clicks"),
    State('input_you', 'value'),
    State('input_rival', 'value')
)
def update_perf(n_clicks, un_you, un_rival):
    if n_clicks==0:
        f = func.empty_fig('no_data')
        r = 'Rating: -'
        hr = 'Highest-Rating: -'
        hp = 'Highest-Performance: -'
        return f, f, r, hr, hp, r, hr, hp
    else:        
        # データが存在するかを確認(存在しない場合は，データが存在しませんと表示する)
        path = f'data/{un_you}/{un_you}_grade.csv'
        path2 = f'data/{un_rival}/{un_rival}_grade.csv'
        is_file = os.path.isfile(path)
        is_file2 = os.path.isfile(path2)               
        if is_file and is_file2:
            # you
            tmp_you = pd.read_csv(f'data/{un_you}/{un_you}_grade.csv', index_col=0)
            trace_list, max_y, un_list = func.make_grade_trace(un_you, trace_list=[], max_y=400, un_list=[])
            fig_tab2 = func.make_grade_fig(trace_list, max_y)
            
            # カードの内容
            r = str(tmp_you['新Rating'].to_list()[0])  # Rating
            hr = str(max(tmp_you['新Rating'].to_list()))  # highest_rating
            hp = str(max(tmp_you['パフォーマンス'].to_list())) # highest_Performance
            r = 'Rating: ' + r
            hr = 'Highest-Rating: ' + hr
            hp = 'Highest-Performance: ' + hp
            
            # rival
            tmp_rival = pd.read_csv(f'data/{un_rival}/{un_rival}_grade.csv', index_col=0)
            trace_list_r, max_y_r, un_list_r = func.make_grade_trace(un_rival, trace_list=[], max_y=400, un_list=[])
            fig_tab2_r = func.make_grade_fig(trace_list_r, max_y_r)
            
            # カードの内容
            r_r = str(tmp_rival['新Rating'].to_list()[0])  # Rating
            hr_r = str(max(tmp_rival['新Rating'].to_list()))  # highest_rating
            hp_r = str(max(tmp_rival['パフォーマンス'].to_list())) # highest_Performance   
            r_r = 'Rating: ' + r_r
            hr_r = 'Highest-Rating: ' + hr_r
            hp_r = 'Highest-Performance: ' + hp_r
        
        
        # youのみデータが存在する場合
        elif is_file:
            # you
            tmp_you = pd.read_csv(f'data/{un_you}/{un_you}_grade.csv', index_col=0)
            trace_list, max_y, un_list = func.make_grade_trace(un_you, trace_list=[], max_y=400, un_list=[])
            fig_tab2 = func.make_grade_fig(trace_list, max_y)
            
            # カードの内容
            r = str(tmp_you['新Rating'].to_list()[0])  # Rating
            hr = str(max(tmp_you['新Rating'].to_list())) # highest_rating
            hp = str(max(tmp_you['パフォーマンス'].to_list())) # highest_Performance
            r = 'Rating: ' + r
            hr = 'Highest-Rating: ' + hr
            hp = 'Highest-Performance: ' + hp
            
            # rival
            fig_tab2_r = func.empty_fig('no_data')
            r_r = 'Rating: -'
            hr_r = 'Highest-Rating: -'
            hp_r = 'Highest-Performance: -'

        # rivalのみデータが存在する場合
        elif is_file2:
            # you
            fig_tab2 = func.empty_fig('no_data')
            r = 'Rating: -'
            hr = 'Highest-Rating: -'
            hp = 'Highest-Performance: -'
            
            # rival
            tmp_rival = pd.read_csv(f'data/{un_rival}/{un_rival}_grade.csv', index_col=0)
            trace_list_r, max_y_r, un_list_r = func.make_grade_trace(un_rival, trace_list=[], max_y=400, un_list=[])
            fig_tab2_r = func.make_grade_fig(trace_list_r, max_y_r)
            
            # カードの内容
            r_r = str(tmp_rival['新Rating'].to_list()[0])  # Rating
            hr_r = str(max(tmp_rival['新Rating'].to_list()))  # highest_rating
            hp_r = str(max(tmp_rival['パフォーマンス'].to_list())) # highest_Performance  
            r_r = 'Rating: ' + r_r
            hr_r = 'Highest-Rating: ' + hr_r
            hp_r = 'Highest-Performance: ' + hp_r         
                        
        else:
            # you
            fig_tab2 = func.empty_fig('no_data')
            r = 'Rating: -'
            hr = 'Highest-Rating: -'
            hp = 'Highest-Performance: -'
            
            # rival
            fig_tab2_r = func.empty_fig('no_data')
            r_r = 'Rating: -'
            hr_r = 'Highest-Rating: -'
            hp_r = 'Highest-Performance: -'

            
        return fig_tab2, fig_tab2_r, r, hr, hp, r_r, hr_r, hp_r
    
#未達成problem
@app.callback(
    Output("unsolve", "children"),
    Input('button_apply', "n_clicks"),
    State('input_you', 'value'),
)
def update_perf(n_clicks, un_you):
    if n_clicks==0:
        table_header2 = [
            html.Thead(html.Tr([html.Th("🚨 未達成Problem 🚨")]), className='table-header')
        ]
        table2 = dbc.Table(
            table_header2,
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            color='primary',
            className='table2'
        )
        return table2

        
    else:        
        df_unsolve = pd.read_csv(f'data/{un_you}/{un_you}_us.csv', index_col=0)
        table_header2 = [
            html.Thead(html.Tr([html.Th("🚨 未達成Problem 🚨")]), className='table-header')
        ]
        list_ = []
        for i in reversed(range(len(df_unsolve))):
            #dropdown_label = df_unsolve.iloc[i, 0] + '_' + df_unsolve.iloc[i, 1]
            num1 = re.findall(r"\d+", df_unsolve.iloc[i, 0])[0]
            num2 = df_unsolve.iloc[i, 1].lower()
            dropdown_label = 'AtCoder Beginner Contest' + num1 + '_' + df_unsolve.iloc[i, 1]
            link = dcc.Link(dropdown_label, href=f'https://atcoder.jp/contests/abc{num1}/tasks/abc{num1}_{num2}', className='link')
            row = html.Tr([html.Td(link, className='td')])
            list_.append(row)
        table_body2 = [html.Tbody(list_)]
        table2 = dbc.Table(
            table_header2 + table_body2,
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            color='primary',
            className='table2'
        )
        return table2


# Battle
@app.callback(
    Output("battle_content", "children"),
    Input('button_apply', "n_clicks"),
    State('input_you', 'value'),
    State('input_rival', 'value')
)
def update_battle(n_clicks, un_you, un_rival):
    if n_clicks==0:
        comp = html.H2('applyしてください！')
        return comp
    else:
        path = f'data/{un_you}/{un_you}_grade.csv'
        path2 = f'data/{un_rival}/{un_rival}_grade.csv'
        is_file = os.path.isfile(path)
        is_file2 = os.path.isfile(path2) 
        if not(is_file) and not(is_file2):
            comp = html.H2('0 - 0', style={'text-align': 'center'}, className='mt-3 mb-3')
            return comp              

        data1 = pd.read_csv(f'data/{un_you}/{un_you}_grade.csv', index_col=0)
        data2 = pd.read_csv(f'data/{un_rival}/{un_rival}_grade.csv', index_col=0)
        
        # 完全な引き分けは考慮しない
        battle_content = [] # 各バトルのコンポーネントを格納
        win1 = 0
        win2 = 0
        for i in range(len(data1)):
            contest = data1.iloc[i, 1]
            if contest in data2['コンテスト'].to_list():
                score1 = data1.iloc[i, 7]
                score2 = data2[data2['コンテスト']==contest]['スコア'][0]
                pena1 = data1.iloc[i, 8]
                pena2 = data2[data2['コンテスト']==contest]['ペナルティ'][0]
                
                time1_1 = data1.iloc[i, 9]
                time1_2 = data1.iloc[i, 10]
                time2_1 = data2[data2['コンテスト']==contest]['タイム(分)'][0]
                time2_2 = data2[data2['コンテスト']==contest]['タイム(秒)'][0]
                time1 = (time1_1 * 60) + time1_2
                time2 = (time2_1 * 60) + time2_2
                
                # 勝敗判定
                if score1 > score2:
                    tmp_win = 1
                    win1 += 1
                elif score1 < score2:
                    tmp_win = 2
                    win2 += 1
                elif time1 < time2:
                    tmp_win = 1
                    win1 += 1
                elif time1 > time2:
                    tmp_win = 2
                    win2 += 1
                elif pena1 < pena2:
                    tmp_win = 1
                    win1 += 1
                elif pena1 > pena2:
                    tmp_win = 2
                    win2 += 1
                
                # コンテスト名コンポーネント
                battle_contest_title = html.Div([
                    html.H4(contest, className='text-center mt-3')
                ])
                battle_content.append(battle_contest_title)
                
                # スコアYou(文字)
                score1_comp = html.Div([
                    html.P('Score' + str(score1), className='win-lose')
                ])
                # スコアRival(文字)
                score2_comp = html.Div([
                    html.P('Score' + str(score2), className='win-lose')
                ])
                
                # バトルバー(全体)
                bar_len1 = 100 * (score1/ (score1+score2))
                bar_len2 = 100 * (score2/ (score1+score2))
                
                if tmp_win == 1:
                    battle_bar = html.Div(
                        [
                            html.Div([
                            score1_comp,
                            html.P('Win', className='win-lose win'),
                            html.P('You', className='bar-you bg-primary text-white', style={'width': f'{bar_len1}%'}),
                            html.P('Rival', className='bar-rival bg-danger text-white', style={'width': f'{bar_len2}%'}),
                            html.P('Lose', className='win-lose lose'),
                            score2_comp,
                            ], className='battle-bar'),
                        ], className='battle-div'
                    )
                else:
                    battle_bar = html.Div(
                        [
                            html.Div([
                            score1_comp,
                            html.P('Lose', className='win-lose win'),
                            html.P('You', className='bar-you bg-primary text-white', style={'width': f'{bar_len1}%'}),
                            html.P('Rival', className='bar-rival bg-danger text-white', style={'width': f'{bar_len2}%'}),
                            html.P('Win', className='win-lose lose'),
                            score2_comp,
                            ], className='battle-bar'),
                        ], className='battle-div'
                    )
                battle_content.append(battle_bar)
                
        battle_results = html.Div([
            html.H1(f'{win1} - {win2}', className='text-center mb-3 mt-3')
        ])
        battle_content.insert(0, battle_results)
        
        return battle_content

    
@app.callback(Output('contents', 'children'), Input('location1', 'pathname'))
def update_page(pathname):
    if pathname == '/new_acquisition':
        return reg#new_acquisition
    elif pathname == '/home':
        return main
    else:
        return main


if __name__ == "__main__":
    app.run_server(debug=True)


