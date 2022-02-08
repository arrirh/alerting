#DAU Feed
#___________________________________________________________________________________________________________________________

query_dau_feed_testing_prop = '''
select q_now.time15, q_now.dau/q_prev.dau as dau_feed
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        count(distinct user_id) as dau, 
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


query_dau_feed_plotting_outlier = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as DAU,
        if(toDate(minutes15) >= today(), 'today', 'yesterday') as day_group
FROM simulator_20220120.feed_actions 
where toDate(time) >= dateadd(day, -1, toDate(now())) and time < now() 
group by minutes15 
order by minutes15
'''


#DAU message
#___________________________________________________________________________________________________________________________

query_dau_mess_testing_prop = '''
select q_now.time15, q_now.dau/q_prev.dau as dau_mess
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        count(distinct user_id) as dau, 
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


query_dau_mess_plotting_outlier = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(distinct user_id) as DAU,
        if(toDate(minutes15) >= today(), 'today', 'yesterday') as day_group
FROM simulator_20220120.message_actions
where toDate(time) >= dateadd(day, -1, toDate(now())) and time < now() 
group by minutes15 
order by minutes15
'''


#All messages
#___________________________________________________________________________________________________________________________

query_message_testing_prop = '''
select q_now.time15, q_now.mess/q_prev.mess as messages
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
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


query_message_plotting_outlier = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        count(user_id) as Messages,
        if(toDate(minutes15) >= today(), 'today', 'yesterday') as day_group
FROM simulator_20220120.message_actions
where toDate(time) >= dateadd(day, -1, toDate(now())) and time < now() 
group by minutes15 
order by minutes15
'''

#All views
#___________________________________________________________________________________________________________________________

query_view_testing_prop = '''
select q_now.time15, q_now.view/q_prev.view as view
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        countIf(action = 'view') as view, 
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
        countIf(action = 'view') as view, 
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


query_view_plotting_outlier = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        countIf(action = 'view') as view,
        if(toDate(minutes15) >= today(), 'today', 'yesterday') as day_group
FROM simulator_20220120.feed_actions 
where toDate(time) >= dateadd(day, -1, toDate(now())) and time < now() 
group by minutes15 
order by minutes15
'''

#All likes
#___________________________________________________________________________________________________________________________


query_like_testing_prop = '''
select q_now.time15, q_now.like/q_prev.like as like
from

(select *, row_number() over(order by time15) rno from

(SELECT toStartOfFifteenMinutes(time) as time15, 
        countIf(action = 'like') as like, 
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
        countIf(action = 'like') as like, 
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


query_like_plotting_outlier = '''
SELECT toStartOfFifteenMinutes(toDateTime(time)) as minutes15, 
        countIf(action = 'like') as like,
        if(toDate(minutes15) >= today(), 'today', 'yesterday') as day_group
FROM simulator_20220120.feed_actions 
where toDate(time) >= dateadd(day, -1, toDate(now())) and time < now() 
group by minutes15 
order by minutes15
'''