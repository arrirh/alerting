# 05-hw-alert

**UPD.** Все необходимые модули установлены, в CI/CD запущен **05.alert.py**.

Финальный вариант системы алертов, которую я хотела использовать, представлен в файле **05.alert.py**, однако в данный момент он не может быть запущен в CI/CD, поскольку в докер-образе отсутствует необходимая библиотека sklearn. Суть моего варианта состоит в использовании трех алгоритмов выявления аномалий. Если как минимум два дадут выявят текущее значение метрики как аномалию, то оно считается аномалией. Первый из алгоритмов (**1**) отдельно реализован в файле **05.simple-prop-alert.py** и запущен в CI/CD, однако сам по себе он показывает достаточно плохой результат, поэтому прошу считать моим решением скрипт **05.alert.py**.


**Описание алгоритма 1 (proportion)**: 
- Рассчитывается отношение метрики за последний прошедший интервал (последняя законченная 15-минутка) к метрике за предпоследний интервал. Предполагается, что такое отношение будет представлять собой величину из нормального распределения со средним в единице, поскольку ожидается, что метрики изменяются плавно. 
- Далее я беру рассчитываю такое отношение для всех 15-минуток, которые относятся к одному и тому же дню недели и имеют одинаковое время. Исходила из предположения о том, что существует как дневная динамика метрик, так и недельная (в каждый день недели может наблюдаться немного иной характер распределения метрик). Также предполагается, что отношение между текущей и предыдущей метрикой должны быть примерно одинаковы на протяжении длительного времени.
- Для отобранных отношений рассчитывается интервал, равный 1.5 межквартильного расстояния. Хотя я предполагаю, что моя величина должна иметь нормальное распределение, по моим наблюдениям интервал в 1.5 IQR позволяет более точно выявлять аномалии, нежели интервал, основанный на расчете среднего и трех стандартных отклонений. Считаю, что это связано с тем, что аномалии смещают значение среднего и стандартного отклонения, отчего их не стоит для поиска аномалий.
- Наблюдения, не попадающие в интервал, считаются аномалиями и репортятся.

**Описание алгоритма 2 (STL)**: 
- Рассчитывается метрика за 15 минут на интервале от текущего момента до начала позапрошлого дня. 
- Применяется STL-декомпозиция получившегося временного ряда. Далее используются остатки.
- Далее выявляются аномалии среди остатков, не входящие в интервал 1.5 IQR.
Оказалось, что этот способ чаще всего выявляет аномалии, которые я определяю таковыми на глаз, при этом крайне редко случаются ложные срабатывания.

**Описание алгоритма 3 (IF)**: 
- Повторяет первые два шага **алгоритма 2**.
- Для поиска аномалий к остаткам применяется метод Isolation Forest.
Такой алгоритм отмечает больше точек как аномалии, чем предыдущий, однако и ошибается он тоже чаще. При применении Isolation Forest непосредственно к исходным метрикам, он не способен учитывать дневную динамику и отмечает ночные снижения как аномалии. Поэтому я применяю его вместе с декомпозицией.



Во время написания системы алертов я также пробовала модель для прогнозирования временных рядов prophet от фэйсбука и алгоритм DBSCAN, однако если последний демонстрирует примерно такую же точность, что Isolation Forest, то у prophet было самое долгое время работы (~10 секунд) при самой низкой точности.


UPD: Все вышеприведенные алгоритмы опирались на идею поиска контекстуальных точечных аномалий, для чего я попыталась максимально абстрагироваться от временной динамики предыдущих дней, и на деле такие алгоритмы оказались не очень успешными. В случае, если изменяется характер распределения метрик, или характер остается прежним, но метрика в принципе становится меньше, то моя система алертов не может это отследить. Возможно, в дальнейшем стоило бы предусмотреть различные ситуации, которые можно считать аномальными.
