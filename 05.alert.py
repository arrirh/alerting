import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns
import pandahouse
import telegram
import io
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

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

chat_id = -655725590
bot = telegram.Bot(token='5181637517:AAEMTMNyqIEjMlr7HKAgPA1OnnoFiw_wf58')


alert_dau_feed = is_alert(query_for_prop = query_feed_proportion, query_for_STL = query_feed_STL, y = 'dau_feed', connection = connection)
alert_view = is_alert(query_for_prop = query_feed_proportion, query_for_STL = query_feed_STL, y = 'view', connection = connection)
alert_like = is_alert(query_for_prop = query_feed_proportion, query_for_STL = query_feed_STL, y = 'like', connection = connection)
alert_ctr = is_alert(query_for_prop = query_feed_proportion, query_for_STL = query_feed_STL, y = 'ctr', connection = connection)

if alert_dau_feed:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'dau_feed', ylab = 'DAU ленты', df = df, plot_title = 'Количество активных пользователей ленты', plot_name = 'dau_feed.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт DAU ленты отправлен')
    
if alert_view:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'view', ylab = 'Количество просмотров', df = df, plot_title = 'Количество просмотров', plot_name = 'view.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт view ленты отправлен')
    
if alert_like:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'like', ylab = 'Количество лайков', df = df, plot_title = 'Количество лайков', plot_name = 'like.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт like ленты отправлен')
    
if alert_ctr:
    df = pandahouse.read_clickhouse(query_feed_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'ctr', ylab = 'CTR', df = df, plot_title = 'CTR', plot_name = 'ctr.png', 
            chat_id = chat_id, bot = bot)
    print('Алерт CTR ленты отправлен')


    
#проверяем метрики мессенджера
#_________________________________________________________________________


alert_dau_mess = is_alert(query_for_prop = query_message_proportion, query_for_STL = query_message_STL, y = 'dau_mess', connection = connection)
alert_messages = is_alert(query_for_prop = query_message_proportion, query_for_STL = query_message_STL, y = 'messages', connection = connection)


if alert_dau_mess:
    df = pandahouse.read_clickhouse(query_message_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'dau_mess', ylab = 'DAU мессенджера', df = df, plot_title = 'Количество активных пользователей мессенджера', plot_name = 'dau_mess.png', 
                tag = '@Some_message_team_member', chat_id = chat_id, bot = bot)
    print('Алерт DAU мессенджера отправлен')
    
if alert_messages:
    df = pandahouse.read_clickhouse(query_message_plotting, connection=connection)
    df = df.iloc[:-1]
    send_report(x = 'minutes15', y = 'messages', ylab = 'Количество сообщений', df = df, plot_title = 'Количество сообщений', plot_name = 'mess.png',
                tag = '@Some_message_team_member', chat_id = chat_id, bot = bot)
    print('Алерт количество сообщений отправлен')
        

#Завершение
#_________________________________________________________________________

print('Скрипт отработал корректно')


