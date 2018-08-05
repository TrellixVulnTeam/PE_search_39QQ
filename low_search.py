import requests, json

# 运行、编辑和复制的url，只需要拼接最后的计划id即可
FIRE = 'http://pec.wps.kingsoft.net/AutotestPlatform/Crontab/Fire/'
EDIT = 'http://pec.wps.kingsoft.net/AutotestPlatform/Crontab/Edit/'
COPY = 'http://pec.wps.kingsoft.net/AutotestPlatform/Crontab/Copy/'

# 获取任务、计划的url
SUBJOBS = 'http://pec.wps.kingsoft.net/AutotestPlatform/ApiV1/filter_subjobs?auth_token=s_hujunjie_3b075b50-6554-40a5-bb02-fba51a1c2fd4'
CRONTABS = 'http://pec.wps.kingsoft.net/AutotestPlatform/ApiV1/get_crontab?auth_token=s_hujunjie_3b075b50-6554-40a5-bb02-fba51a1c2fd4&id='

# 访问任务url的参数
SUBJOBS_PARAMS = {
    'StartTime': '2018-08-01 00:00:00',
    'EndTime': '2018-08-02 00:00:00',
    'TaskName': None,
    'ToolName': None,
    'UserName': None,
}

# 访问计划url的参数
CRONTABS_PARAMS = {
    'id': None,
}

def get_subjobs_params(start_time, end_time, task_name=None, tool_name=None, user_name=None):
    params = SUBJOBS_PARAMS
    params['StartTime'] = start_time
    params['EndTime'] = end_time
    params['TaskName'] = task_name
    params['ToolName'] = tool_name
    params['UserName'] = user_name
    return params

# print(get_subjobs_params('1', '2', '3', '4', '5'))

# resp = requests.post(SUBJOBS, data=json.dumps(get_subjobs_params('2018-08-01 00:00:00', '2018-08-02 20:40:00', tool_name='SAK', user_name='s_hujunjie')))
# print(resp.json())

# resp = requests.get(CRONTABS)
# print(resp.json())

# 存储计划id的list，记得去重
id_list = list()
# list<map>，每一项存的是id和name
id_name_map_list = list()
# 获取id
resp = requests.post(SUBJOBS, data=json.dumps(get_subjobs_params('2018-08-01 00:00:00', '2018-08-02 20:40:00', tool_name='SAK', user_name='s_hujunjie')))
# print(json.loads(resp.json()))
for subjob in json.loads(resp.json())['subjobs']:
    id_list.append(dict(subjob)['CrontabId'])

# 去重
id_list = list(set(id_list))
print(id_list)

for id in id_list:
    resp = requests.get(CRONTABS + str(id))
    print(resp.json())