import os
os.system('pip install statsmodels')

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import pandahouse
import telegram
import io


connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator'
}

q = "\
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, \
        count(distinct user_id) as DAU \
FROM simulator_20220120.feed_actions \
where toDate(time) >= dateadd(day, -1, toDate(now())) and time < now() \
group by minutes15 \
order by minutes15 desc"

df = pandahouse.read_clickhouse(q, connection=connection)
df = df.iloc[1:]

datetime_series = pd.to_datetime(df.minutes15)
datetime_index = pd.DatetimeIndex(datetime_series.values)

df2=df.set_index(datetime_index)
df2.drop('minutes15',axis=1,inplace=True)

result = seasonal_decompose(df2, period = 2, model='additive')

q75, q25 = np.nanpercentile(result.resid.values, [75 ,25])
iqr = q75 - q25
lower = q25 - 1.5*iqr
upper = q75 + 1.5*iqr
is_outlier = np.logical_or(result.resid.values > upper, result.resid.values < lower)

is_alert = is_outlier[len(is_outlier) - 1]

chat_id = 329018735
bot = telegram.Bot(token='5181637517:AAEMTMNyqIEjMlr7HKAgPA1OnnoFiw_wf58')

current_value = df.DAU[1]

if is_alert:
    msg = f'Метрика DAU:\nтекущее значение = {current_value}\nотклонение от вчера ()'

    sns.set(rc={'figure.figsize': (16, 10)}) # задаем размер графика
    plt.tight_layout()

    fig, ax = plt.subplots()
    ax.plot_date(data = df, x = 'minutes15', y = 'DAU', linestyle = '--')

    # формируем файловый объект
    plot_object = io.BytesIO()
    ax.figure.savefig(plot_object)
    plot_object.seek(0)
    plot_object.name = 'dau.png'
    plt.close()

    # отправляем алерт
    bot.sendMessage(chat_id=chat_id, text=msg)
    bot.sendPhoto(chat_id=chat_id, photo=plot_object)


