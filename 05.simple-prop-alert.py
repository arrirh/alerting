import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
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

#проверяем метрики ленты
#_________________________________________________________________________


df = pandahouse.read_clickhouse(query_feed_proportion, connection=connection)

is_alert_prop_dau = is_outliers_IQR(df, 'time15', 'dau_feed')
is_alert_prop_view = is_outliers_IQR(df, 'time15', 'view')
is_alert_prop_like = is_outliers_IQR(df, 'time15', 'like')
is_alert_prop_ctr = is_outliers_IQR(df, 'time15', 'ctr')

if is_alert_prop_dau:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'DAU', ylab = 'DAU', df = df, plot_title = 'Количество активных пользователей ленты', plot_name = 'dau_feed.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт DAU ленты отправлен')
    
if is_alert_prop_view:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'view', ylab = 'Количество просмотров', df = df, plot_title = 'Количество просмотров', plot_name = 'view.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт DAU ленты отправлен')
    
if is_alert_prop_like:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'like', ylab = 'Количество лайков', df = df, plot_title = 'Количество лайков', plot_name = 'like.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт DAU ленты отправлен')
    
if is_alert_prop_ctr:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'ctr', ylab = 'CTR', df = df, plot_title = 'CTR', plot_name = 'ctr.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт DAU ленты отправлен')

#проверяем метрики мессенджера
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

    

#Завершение
#_________________________________________________________________________

print('Скрипт отработал корректно')
