import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandahouse
import telegram
import io
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

def is_outliers_IQR(metric):
    q75, q25 = np.nanpercentile(metric, [75 ,25])
    iqr = q75 - q25
    lower = q25 - 1.5*iqr
    upper = q75 + 1.5*iqr
    is_outliers = np.logical_or(metric > upper, metric < lower)
    return is_outliers[len(is_outliers) - 1]

def is_alert(query_for_prop, query_for_STL, y, connection):
    #1
    df = pandahouse.read_clickhouse(query_for_prop, connection=connection)

    is_alert_prop = is_outliers_IQR(df[y])

    #2
    df = pandahouse.read_clickhouse(query_for_STL, connection=connection)

    df = df[['minutes5', y]]
    datetime_series = pd.to_datetime(df['minutes5'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)

    df_for_STL = df.set_index(datetime_index)
    df_for_STL.drop('minutes5', axis = 1, inplace = True)

    result = seasonal_decompose(df_for_STL, period = 2, model='additive')

    is_alert_resid = is_outliers_IQR(result.resid.values)

    #3
    scaler = StandardScaler()
    np_scaled = scaler.fit_transform(df_for_STL.values.reshape(-1, 1))
    data = pd.DataFrame(np_scaled)
    model =  IsolationForest()
    model.fit(data) 

    is_alert_IF = (model.predict(data) == -1)[-1]

    return int(is_alert_prop) + int(is_alert_resid) + int(is_alert_IF) >= 2


def send_report(x, y, ylab, plot_title, plot_name, df, chat_id, bot,
                hue = 'day_group', xlim_filter = 'Сегодня', xlab = 'Время', legend_title = 'День', legend_labels = ['Неделю назад', 'Вчера', 'Сегодня'],
                tag = '@some_feed_team_member', figsize = (12, 8), fontsize = 14):
    df['time'] = df[x].apply(lambda x: x.time()) #преобразование времени для графика
    df['time'] = pd.to_datetime(df.time, format = '%H:%M:%S')

    plt.rc('figure',figsize = figsize)
    plt.rc('font', size = fontsize)
    ax = plt.gca()

    sns.lineplot(ax = ax, data = df, x = 'time', y = y, hue = hue, ci = None, marker = 'o') #строим график

    formatter = mdates.DateFormatter("%H:%M:%S") #настройка оси x так, чтобы показывалось время
    ax.xaxis.set_major_formatter(formatter)

    plt.xticks(rotation=45)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend(title = legend_title, labels = legend_labels)
    plt.title(plot_title)
    plt.xlim(left = df['time'][df[hue] == xlim_filter].min(), right = df['time'][df[hue] == xlim_filter].max()) #диапазон времени от полуночи до времени последней пятнадцатиминутки сегодня

    current_value = df[y].iloc[-1]
    prev_value = df[y][df['time'] == df['time'].iloc[-1]].iloc[0]
    diff = 100 - round(min(current_value, prev_value)/max(current_value, prev_value), 2) * 100
    text = f'Метрика {ylab}:\nТекущее значение = {current_value}. Предыдущее значение = {prev_value}.\nОтклонение более {diff}%.\n{tag}'


    plot_object = io.BytesIO() #открываем буфер
    plt.savefig(plot_object, bbox_inches = 'tight') #сохраняем график в буфер
    plot_object.name = plot_name #называем файл
    plot_object.seek(0) #?
    plt.close() #закрываем график

    media_group = []
    media_group.append(telegram.InputMediaPhoto(plot_object, caption = text)) 

    bot.send_media_group(chat_id = chat_id, media = media_group)
