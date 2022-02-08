import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import pandahouse
import telegram
import io

from alert_utils import *
from alert_queries import *

#Init
#_________________________________________________________________________

connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator'
}

chat_id = 329018735
bot = telegram.Bot(token='5181637517:AAEMTMNyqIEjMlr7HKAgPA1OnnoFiw_wf58')

#проверяем DAU ленты
#_________________________________________________________________________


df = pandahouse.read_clickhouse(query_dau_feed_testing_prop, connection=connection)

is_alert_prop = is_outliers_IQR(df, 'time15', 'dau_feed')

if is_alert_prop:
    df = pandahouse.read_clickhouse(query_dau_feed_plotting_outlier, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'DAU', ylab = 'DAU', df = df, plot_title = 'Количество активных пользователей ленты', plot_name = 'dau_feed.png')
    print('Алерт DAU ленты отправлен')

#проверяем DAU мессенджера
#_________________________________________________________________________


df = pandahouse.read_clickhouse(query_dau_mess_testing_prop, connection=connection)

is_alert_prop = is_outliers_IQR(df, 'time15', 'dau_mess')

if is_alert_prop:
    df = pandahouse.read_clickhouse(query_dau_mess_plotting_outlier, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'DAU', ylab = 'DAU', df = df, plot_title = 'Количество активных пользователей мессенджера', plot_name = 'dau_mess.png', 
                tag = '@Some_message_team_member')
    print('Алерт DAU мессенджера отправлен')
    

#проверяем количество сообщений
#_________________________________________________________________________


df = pandahouse.read_clickhouse(query_message_testing_prop, connection=connection)

is_alert_prop = is_outliers_IQR(df, 'time15', 'messages')

if is_alert_prop:
    df = pandahouse.read_clickhouse(query_message_plotting_outlier, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'Messages', ylab = 'Количество сообщений', df = df, plot_title = 'Количество сообщений', plot_name = 'mess.png',
                tag = '@Some_message_team_member')
    print('Алерт количества сообщений отправлен')

    
#проверяем просмотры
#_________________________________________________________________________


df = pandahouse.read_clickhouse(query_view_testing_prop, connection=connection)

is_alert_prop = is_outliers_IQR(df, 'time15', 'view')

if is_alert_prop:
    df = pandahouse.read_clickhouse(query_view_plotting_outlier, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'view', ylab = 'Количество просмотров', df = df, plot_title = 'Количество просмотров', plot_name = 'view.png')
    print('Алерт количества просмотров отправлен')
    
    
#проверяем лайки
#_________________________________________________________________________


df = pandahouse.read_clickhouse(query_like_testing_prop, connection=connection)

is_alert_prop = is_outliers_IQR(df, 'time15', 'like')

if is_alert_prop:
    df = pandahouse.read_clickhouse(query_like_plotting_outlier, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'like', ylab = 'Количество лайков', df = df, plot_title = 'Количество лайков', plot_name = 'like.png')
    print('Алерт количества лайков отправлен')


#Завершение
#_________________________________________________________________________

print('Скрипт отработал корректно')