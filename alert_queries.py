#Feed proportion query
#___________________________________________________________________________________________________________________________

query_feed_proportion = '''
select q_now.time15 as minutes15, q_now.dau/q_prev.dau as dau_feed, q_now.view/q_prev.view as view, q_now.like/q_prev.like as like, q_now.ctr/q_prev.ctr as ctr
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        count(distinct user_id) as dau,
        countIf(action = 'view') as view,
        countIf(action = 'like') as like,
        countIf(action = 'like')/countIf(action = 'view') as ctr,
        toDayOfWeek(time15) as day_of_week, 
        toHour(time15) as hour, 
        toMinute(time15) as minute
from simulator_20220120.feed_actions 
group by time15
order by time15 desc) q1

inner join 

(select * from (SELECT toStartOfFifteenMinutes(time) as time15, 
                        toDayOfWeek(time15) as day_of_week, 
                        toHour(time15) as hour, 
                        toMinute(time15) as minute
                FROM simulator_20220120.feed_actions
                WHERE time >= toDateTime(toStartOfDay(now()))
                  AND time < now()
                GROUP BY time15
                ORDER BY time15 DESC
                limit 2)
order by time15 asc limit 1) q2

on q1.day_of_week = q2.day_of_week and q1.hour = q2.hour and q1.minute = q2.minute) q_now


join



(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        count(distinct user_id) as dau,
        countIf(action = 'view') as view,
        countIf(action = 'like') as like,
        countIf(action = 'like')/countIf(action = 'view') as ctr,
        toDayOfWeek(time15) as day_of_week, 
        toHour(time15) as hour, 
        toMinute(time15) as minute
from simulator_20220120.feed_actions 
group by time15
order by time15 desc) q1

inner join 

(select time15, 
        day_of_week, 
        hour, 
        if(minute = 0, 45, minute - 15) as minute
from (SELECT toStartOfFifteenMinutes(time) as time15, 
                        toDayOfWeek(time15) as day_of_week, 
                        toHour(time15) as hour, 
                        toMinute(time15) as minute
                FROM simulator_20220120.feed_actions
                WHERE time >= toDateTime(toStartOfDay(now()))
                  AND time < now()
                GROUP BY time15
                ORDER BY time15 DESC
                limit 2)
order by time15 asc limit 1)q2

on q1.day_of_week = q2.day_of_week and q1.hour = q2.hour and q1.minute = q2.minute) q_prev

on q_now.rno = q_prev.rno
'''

#Feed plotting query
#___________________________________________________________________________________________________________________________

query_feed_plotting = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as dau_feed,
        countIf(action = 'view') as view,
        countIf(action = 'like') as like,
        countIf(action = 'like')/countIf(action = 'view') as ctr,
        'Неделю назад' as day_group
FROM simulator_20220120.feed_actions 
where toDate(time) = toDate(dateadd(day, -7, toDate(now()))) 
group by minutes15 
order by minutes15

union all

SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as DAU,
        countIf(action = 'view') as view,
        countIf(action = 'like') as like,
        countIf(action = 'like')/countIf(action = 'view') as ctr,
        'Вчера' as day_group
FROM simulator_20220120.feed_actions 
where toDate(time) = toDate(dateadd(day, -1, toDate(now()))) 
group by minutes15 
order by minutes15

union all

SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as DAU,
        countIf(action = 'view') as view,
        countIf(action = 'like') as like,
        countIf(action = 'like')/countIf(action = 'view') as ctr,
        'Сегодня' as day_group
FROM simulator_20220120.feed_actions 
where toDate(time) = toDate(now()) 
group by minutes15 
order by minutes15
'''


#Message proportion query
#___________________________________________________________________________________________________________________________

query_message_proportion = '''
select q_now.time15 as minutes15, q_now.dau/q_prev.dau as dau_mess, q_now.mess/q_prev.mess as messages
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        count(distinct user_id) as dau, 
        count(user_id) as mess,
        toDayOfWeek(time15) as day_of_week, 
        toHour(time15) as hour, 
        toMinute(time15) as minute
from simulator_20220120.message_actions
group by time15
order by time15 desc) q1

inner join 

(select * from (SELECT toStartOfFifteenMinutes(time) as time15, 
                        toDayOfWeek(time15) as day_of_week, 
                        toHour(time15) as hour, 
                        toMinute(time15) as minute
                FROM simulator_20220120.message_actions
                WHERE time >= toDateTime(toStartOfDay(now()))
                  AND time < now()
                GROUP BY time15
                ORDER BY time15 DESC
                limit 2)
order by time15 asc limit 1) q2

on q1.day_of_week = q2.day_of_week and q1.hour = q2.hour and q1.minute = q2.minute) q_now


join




(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        count(distinct user_id) as dau, 
        count(user_id) as mess,
        toDayOfWeek(time15) as day_of_week, 
        toHour(time15) as hour, 
        toMinute(time15) as minute
from simulator_20220120.message_actions
group by time15
order by time15 desc) q1

inner join 

(select time15, 
        day_of_week, 
        hour, 
        if(minute = 0, 45, minute - 15) as minute
from (SELECT toStartOfFifteenMinutes(time) as time15, 
                        toDayOfWeek(time15) as day_of_week, 
                        toHour(time15) as hour, 
                        toMinute(time15) as minute
                FROM simulator_20220120.message_actions
                WHERE time >= toDateTime(toStartOfDay(now()))
                  AND time < now()
                GROUP BY time15
                ORDER BY time15 DESC
                limit 2)
order by time15 asc limit 1)q2

on q1.day_of_week = q2.day_of_week and q1.hour = q2.hour and q1.minute = q2.minute) q_prev

on q_now.rno = q_prev.rno
'''



#Message plotting query
#___________________________________________________________________________________________________________________________

query_message_plotting = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as dau_mess,
        count(user_id) as messages,
        'Неделю назад' as day_group
FROM simulator_20220120.message_actions 
where toDate(time) = toDate(dateadd(day, -7, toDate(now()))) 
group by minutes15 
order by minutes15

union all

SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as DAU,
        count(user_id) as messages,
        'Вчера' as day_group
FROM simulator_20220120.message_actions 
where toDate(time) = toDate(dateadd(day, -1, toDate(now()))) 
group by minutes15 
order by minutes15

union all

SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as DAU,
        count(user_id) as messages,
        'Сегодня' as day_group
FROM simulator_20220120.message_actions 
where toDate(time) = toDate(now()) 
group by minutes15 
order by minutes15
'''

#Feed STL query
#___________________________________________________________________________________________________________________________

query_feed_STL = '''
SELECT toStartOfFiveMinute(toDateTime(time)) as minutes5, 
        count(distinct user_id) as dau_feed,
        countIf(action = 'view') as view,
        countIf(action = 'like') as like,
        countIf(action = 'like')/countIf(action = 'view') as ctr
FROM simulator_20220120.feed_actions 
where toDate(time) >= toDate(dateadd(day, -2, toDate(now()))) and time < now()
group by minutes5 
order by minutes5
'''

#Feed STL query
#___________________________________________________________________________________________________________________________

query_message_STL = '''
SELECT toStartOfFiveMinute(toDateTime(time)) as minutes5, 
        count(distinct user_id) as dau_mess,
        count(user_id) as messages
FROM simulator_20220120.message_actions 
where toDate(time) >= toDate(dateadd(day, -2, toDate(now()))) and time < now()
group by minutes5 
order by minutes5
'''