# -*- coding: utf-8 -*-

import csv
import codecs
import decimal

path_pomodone_log = 'pomodone-log.csv'
rfile_pomodone_log = codecs.open(path_pomodone_log, 'rb', encoding="utf-8")
csv_pomodone_log = csv.DictReader(rfile_pomodone_log, delimiter=',')

dict_task = {}
dict_time = {}
dict_count = {}
dict_label = {}

list_test = []

task_date = ""
task_date_temp = ""
count_date = 0

for temp in csv_pomodone_log:
    task_id = temp['permalink'][temp['permalink'].find('c/') + 2:]
    if task_date_temp == str(temp['date']):
        pass
    else:
        task_date_temp = str(temp['date'])
        count_date += 1
    if len(task_id) == 0:
        continue
    task_time = (
        int(temp['time spent'][:2]) * 60 * 60 +
        int(temp['time spent'][3:5]) * 60 +
        int(temp['time spent'][7:]))
    # 項目
    try:
        test = dict_task[task_id]
    except KeyError:
        dict_task[task_id] = task_id
    # 時間
    try:
        test = dict_time[task_id]
        task_time_temp = dict_time[task_id]
        dict_time[task_id] = task_time_temp + task_time
    except KeyError:
        dict_time[task_id] = task_time
    # 計數
    if int(temp['time spent'][:2]) * 60 * 60 > 1500:
        counter = 2
    else:
        counter = 1
    try:
        test = dict_time[task_id]
        task_count_temp = dict_count[task_id]
        dict_count[task_id] += counter
    except KeyError:
        dict_count[task_id] = counter
    # 標籤
    try:
        test = dict_label[task_id]
    except KeyError:
        dict_label[task_id] = task_id
    try:
        list_test.index(task_id)
    except ValueError:
        list_test.append(task_id)

path_trello_archived = 'Archived trello.csv'
rfile_trello_archived = codecs.open(
    path_trello_archived, 'rb', encoding="utf-8")
csv_trello_archived = csv.DictReader(rfile_trello_archived, delimiter=',')

for temp in csv_trello_archived:
    task_id = temp['Card URL'][temp['Card URL'].find('c/') + 2:]
    if len(task_id) == 0:
        continue
    try:
        test = dict_task[task_id]
        task_title = temp['Title'][temp['Title'].find('] ') + 2:]
        task_label = temp['Labels']
        # 項目
        dict_task[task_id] = task_title
        dict_label[task_id] = task_label
    except KeyError:
        pass

path_trello = 'trello.csv'
rfile_trello = codecs.open(path_trello, 'rb', encoding="utf-8")
csv_trello = csv.DictReader(rfile_trello, delimiter=',')

for temp in csv_trello:
    task_id = temp['Card URL'][temp['Card URL'].find('c/') + 2:]
    try:
        test = dict_task[task_id]
        task_title = temp['Title']
        task_label = temp['Labels']
        # 項目
        dict_task[task_id] = task_title
        dict_label[task_id] = task_label
    except KeyError:
        pass

path_output = 'output.csv'
write_output = codecs.open(path_output, 'w', encoding='utf-8')
write_output.write('id,工項,工時(秒),工時(分),日均(分),工時(時),工時(天),執行次數,標籤\n')


def wfile_output(task_id, task, time, count, labels):
    write_output.write('"' + str(task_id) + '",')
    write_output.write('"' + str(task) + '",')
    write_output.write('"' + str(time) + '",')
    write_output.write('"' + str(decimal.Decimal(time / 60).quantize(decimal.Decimal('0.01'))) + '",')
    write_output.write('"' + str(decimal.Decimal(time / 60 / count_date).quantize(decimal.Decimal('0.01'))) + '",')
    write_output.write('"' + str(decimal.Decimal(time / 60 / 60).quantize(decimal.Decimal('0.01'))) + '",')
    write_output.write('"' + str(decimal.Decimal(time / 60 / 60 / 24).quantize(decimal.Decimal('0.01'))) + '",')
    write_output.write('"' + str(count) + '",')
    write_output.write('"' + str(labels) + '"\n')


for temp in dict_task:
    wfile_output(
        temp,
        dict_task[temp],
        dict_time[temp],
        dict_count[temp],
        dict_label[temp])

print(count_date)
