import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import datetime
from datetime import timedelta
import os
import time
import datetime
from selenium.webdriver import Chrome, ChromeOptions
import re
import time
import numpy as np
import pandas as pd
import cnum
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State
import dash_daq as daq
from selenium.webdriver.chrome import service as fs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from tqdm.notebook import tqdm
import pandas.tseries.offsets as offsets  # pandasのtimestampを1日ずらすため
import pandas as pd
from pandas import DataFrame, Series
import datetime
from datetime import timedelta
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from collections import defaultdict
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

CHROMEDRIVER = "./chromedriver"

# t: タイトル 問題種別正解数(ABC)
def empty_fig(t):
    # ユーザーデータが存在しない場合に表示するfigure
    no_data_fig = go.Figure()
    no_data_fig.update_layout(
        annotations=[
            go.layout.Annotation(
                xref='paper',
                yref='paper',
                x=0.5,
                y=0.5,
                showarrow=False,
                text='データがありません',
                font={'size': 20}
            ),
        ],
        modebar_remove=[
            'zoom2d',  # ズームモード
            'pan2d',  # 移動モード
            'select2d',  # 四角形で選択
            'lasso2d',  # ラッソで選択
            'zoomIn2d',  # 拡大
            'zoomOut2d',  # 縮小
            'autoScale2d',  # 自動範囲設定
            'resetScale2d',  # 元の縮尺
        ],
    )
    return no_data_fig


def get_datelist(df):
    start = datetime.datetime.strptime(df.iloc[0, 0][:10], "%Y-%m-%d")
    start = datetime.date(start.year, start.month, start.day)
    end = datetime.date.today()
    
    # for文で日付リストを作成
    date_list = []
    for i in range((end - start).days + 1):
        date = start + timedelta(i)
        date_list.append(date)
        
    return date_list

def get_ansnum(df):
    start = datetime.datetime.strptime(df.iloc[0, 0][:10], "%Y-%m-%d")
    start = datetime.date(start.year, start.month, start.day)
    end = datetime.date.today()
    ans_num = []

    for i in range((end - start).days + 1):
        date = start + timedelta(i)

        # 提出結果dfの提出日時からdate型のリストを作る
        df_date = []
        for j in df['提出日時'].to_list():
            tmp_date = datetime.datetime.strptime(j[:10], "%Y-%m-%d")
            tmp_date = datetime.date(tmp_date.year, tmp_date.month, tmp_date.day)
            df_date.append(tmp_date)

        num = df_date.count(date)
        ans_num.append(num)
    
    return ans_num

def make_fig1(df, templete='bootstrap'):
    list_x = get_datelist(df)
    list_y = get_ansnum(df)
    
    layout = go.Layout(
        # title={
        #     'text': '日別提出数(AtCoder Beginner Contest)'
        # },
        xaxis={
            'rangeslider': {'visible': False},
            'rangeselector': {
                'buttons': [
                    {'label': '1month', 'step': 'month', 'count': 1},
                    {'label': '7days', 'step': 'day', 'count': 7},
                    {'step': 'all'},
                ]
            },
        },
        yaxis={'title': {'text': 'Number of Submissions', 'font': {'family': 'Times New Roman', 'size': 20}}},
        margin={'l': 50, 'r': 35, 'b': 35, 't': 35},
    )
    
    trace = go.Bar(x=list_x, y=list_y)
    fig = go.Figure(trace, layout = layout)
    
    fig.update_layout(
        modebar_remove=[
            'zoom2d',  # ズームモード
            'pan2d',  # 移動モード
            'select2d',  # 四角形で選択
            'lasso2d',  # ラッソで選択
            'zoomIn2d',  # 拡大
            'zoomOut2d',  # 縮小
            'autoScale2d',  # 自動範囲設定
            'resetScale2d',  # 元の縮尺
        ],
        # plot_bgcolor='rgba(182, 234, 250, 0.9)',
    )

    
    return fig

def get_streaks(data):
    # data = data.sort_values('提出日時')
    ans_num = get_ansnum(data)
    
    max_streak = 0
    now_streak = 0
    sub_y = 0
    tmp_streak = 0

    for i in ans_num:
        if i > 0:
            tmp_streak += 1
        elif i == 0:
            max_streak = max(max_streak, tmp_streak)
            tmp_streak = 0

    tmp_streak = 0
    for i in reversed(ans_num):
        if i == 0:
            now_streak = tmp_streak
            break
        elif i > 0:
            tmp_streak += 1

    sub_y = ans_num[-1]
    
    return max_streak, now_streak, sub_y



def make_grade_trace(un, trace_list=[], max_y=200, un_list=[]):
    df_grade = pd.read_csv(f'data/{un}/{un}_grade.csv', index_col=0)
    # パフォーマンスとレーティングの推移を可視化
    trace_rating = go.Scatter(x=list(reversed(df_grade['日付'].to_list())), y=list(reversed(df_grade['新Rating'].to_list())),\
                             name=f'{un}(Rating)', marker={'size': 13, 'symbol': 'diamond'})
    trace_performance = go.Scatter(x=list(reversed(df_grade['日付'].to_list())), y=list(reversed(df_grade['パフォーマンス'].to_list())),\
                                  name=f'{un}(Performance)', marker={'size': 13, 'symbol': 'diamond'})
    
    trace_list.append(trace_rating)
    trace_list.append(trace_performance)
    
    tmp1 = max(df_grade['パフォーマンス'].to_list())
    tmp2 = max(df_grade['新Rating'].to_list())
    tmp = max(tmp1, tmp2)
    if tmp > max_y:
        max_y = tmp
        
    un_list.append(un)
    #max_list.append(tmp)
    
    return trace_list, max_y, un_list

def make_grade_fig(trace_list, max_y):
    color_list = ['#a9a9a9', '#8b4513', '#228b22', '#87ceeb', '#0000cd', '#ffd700', '#ff8c00', '#ff0000']
    rating_below = [-10, 400, 800, 1200, 1600, 2000, 2400, 2800]
    rating_upper = [400, 800, 1200, 1600, 2000, 2400, 2800, 3200]
    shape_list = []

    for color, below, upper in zip(color_list, rating_below, rating_upper):
        shape = go.layout.Shape(
                type='rect',
                xref='paper',
                yref='y',
                x0=0,
                x1=1,
                y0=below,
                y1=upper,
                fillcolor=color,
                #fillcolor='rgb(239, 85, 59)',
                opacity=0.25,
                layer='below',
                line={'width': 0}
        )
        shape_list.append(shape)

    layout = go.Layout(
        shapes = shape_list,
        modebar_remove=[
            'zoom2d',  # ズームモード
            'pan2d',  # 移動モード
            'select2d',  # 四角形で選択
            'lasso2d',  # ラッソで選択
            'zoomIn2d',  # 拡大
            'zoomOut2d',  # 縮小
            'autoScale2d',  # 自動範囲設定
            'resetScale2d',  # 元の縮尺
        ],
        yaxis={'zeroline': False},
        margin={'l': 50, 'r': 35, 'b': 35, 't': 35}
    )

    fig = go.Figure(trace_list, layout=layout)
    fig.update_yaxes(range=[-10, max_y+50])
    fig.update_xaxes(showgrid=False)
    fig.update_layout(legend_orientation='h')

    return fig