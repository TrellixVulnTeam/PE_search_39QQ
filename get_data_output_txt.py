import requests, json

CRONTAB_URL = 'http://pec.wps.kingsoft.net/AutotestPlatform/ApiV1/get_crontab?auth_token=s_hujunjie_3b075b50-6554-40a5-bb02-fba51a1c2fd4&id='
TASK_URL = 'http://pec.wps.kingsoft.net/AutotestPlatform/ApiV1/get_task?auth_token=s_hujunjie_3b075b50-6554-40a5-bb02-fba51a1c2fd4&id='

with open('crontab_data.txt', 'a', encoding='utf-8') as f:
    f.write('[')
    for i in range(1001881, 1001981):
        response = requests.get(CRONTAB_URL + str(i))
        f.write(response.json() + ',')
        print('crontag:' + str(i))
    f.write(']')

with open('task_data.txt', 'a', encoding='utf-8') as f:
    f.write('[')
    for i in range(1020541, 1020641):
        response = requests.get(TASK_URL + str(i))
        f.write(response.json() + ',')
        print('task:' + str(i))
    f.write(']')