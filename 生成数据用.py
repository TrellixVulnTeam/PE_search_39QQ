import json

# 解析计划json，提取有用的数据提交给elasticsearch

f = open('crontab_data.txt', 'r', encoding='utf-8')
crontab_data = f.read()
f.close()

f = open('task_data.txt', 'r', encoding='utf-8')
task_data = f.read()
f.close()

# # print(first_data)

# for crontab in json.loads(first_data):
#     print(crontab)

# 计划有用的字段
def get_data_crontab(crontab):
    data = dict()
    try:
        # 计划id
        data['Id'] = crontab['Id']
        # 计划类型，wps，wpp，et
        data['Type'] = crontab['TestProduct']['Type']
        # 分支
        data['Branch'] = _replace(crontab['TestProduct']['WpsProduct']['Branch']) + ' ' + crontab['TestProduct']['WpsProduct']['Branch']
        # 版本
        data['Edition'] = _replace(crontab['TestProduct']['WpsProduct']['Edition']) + ' ' + crontab['TestProduct']['WpsProduct']['Edition']
        # 计划名
        data['Name'] = _replace(crontab['Name']) + ' ' + crontab['Name']
        # PE平台分类
        data['Path'] = _replace(crontab['Path']) + ' ' + crontab['Path']
        # 关注人邮箱
        data['SubscribersMail'] = _replace(crontab['SubscribersMail'])
        # 计划是否启用
        data['Disabled'] = crontab['Disabled']
        return data
    except:
        pass

# 任务有用的字段
def get_data_task(task):
    data = dict()
    try:
        # 任务id
        data['Id'] = task['Id']
        # 计划id
        data['CrontabId'] = task['CrontabId']
        # 任务名
        data['TaskName'] = _replace(task['TaskName']) + ' ' + task['TaskName']
        # 任务工具
        data['ToolName'] = task['ToolName']
        # 任务是否可用
        data['Disabled'] = task['Disabled']
        # 任务备注
        data['Note'] = _replace(task['Note'])
        # 获取步骤的类型以及运行程序的配置文件和获取样张的路径
        # 列表，存储步骤的列表，每一项是一个字典
        data['Type'] = ''
        data['SrcPath'] = ''
        for subtask in task['ExtraInfo']['Subtasks']:
            data['Type'] = data['Type'] + subtask['Type'] + ' '
            if subtask['Type'] == 'CopyTask':
                for info in subtask['_Subtask']['CopyInfoList']:
                    data['SrcPath'] = data['SrcPath'] + _replace(info['SrcPath']) + ' '
            elif subtask['Type'] == 'RunProgramTask':
                info_list = subtask['_Subtask']['Parameters']
                for i in range(0, len(info_list), 2):
                    if info_list[i] == '--testcaseconfig':
                        data['testcaseconfig'] = info_list[i+1]
                        break
        return data
    except:
        pass

def _replace(string):
    data = str(string)
    data = data.replace('_', ' ')
    data = data.replace('-', ' ')
    data = data.replace(';', ' ')
    data = data.replace('/', ' ')
    data = data.replace('【', '')
    data = data.replace('】', ' ')
    data = data.replace('\n', ' ')
    data = data.replace('\"', ' ')
    # data = data.replace(':', ' ')
    # data = data.replace('：', ' ')
    data = data.replace('\\\\', '\\')
    data = data.replace('，', ' ')
    data = data.replace(',', ' ')
    return data

for crontab in json.loads(crontab_data):
    get_data_crontab(crontab)

for task in json.loads(task_data):
    get_data_task(task)