import json
from elasticsearch import Elasticsearch
from 生成数据用 import get_data_task, get_data_crontab

# doc = [
#      {"index": {"_id": 1}},
#      {"name": "python", "addr": "惠东"},
#      {"index": {"_id": 2}},
#      {"name": "java", "addr": "惠州"},
#      {"index": {"_id": 3}},
#      {"name": "kotlin", "addr": "从化"},
#      {"index": {"_id": 4}},
#      {"name": "android", "addr": "广州"},
#  ]

doc = {
    'Id': '1001979',
    'Type': 'WpsProduct',
    'Branch': 'func v10 trunk branch func_v10_trunk_branch',
    'Edition': 'Professional VBA Professional_VBA',
    'Name': 'Core WPS 排版大数据   新人测试用 【Core】WPS-排版大数据 - 新人测试用',
    'Path': '新人熟悉工具专用 图片比较工具 新人熟悉工具专用/图片比较工具',
    'SubscribersMail': '',
    'Disabled': 'False'
}

doc_1 = {
    'Id': '1001920',
    'Type': 'WpsProduct',
    'Branch': 'rc v11 personal kprometheus 20180615 branch rc_v11_personal_kprometheus_20180615_branch',
    'Edition': 'PersonalDownload Trial PersonalDownload_Trial',
    'Name': 'WPP 日常 新性能监控 2019  【WPP】日常_新性能监控_2019 ',
    'Path': '2019计划 2019计划',
    'SubscribersMail': 'chentingting1@wps.cn',
    'Disabled': 'False'
}

task_doc = {
  'Id': '1020542',
  'CrontabId': '1001979',
  'TaskName': '000 字符排版 单一读盘 排序 000-字符排版-单一读盘-排序',
  'ToolName': '字符排版',
  'Disabled': 'False',
  'Note': '工具流程  基线 WPS稳定版打开 打印XPS 测试 WPS新版打开 打印XPS 与基线XPS对比产生差异图片 ',
  'Type': 'SvnExportTask CopyTask RunProgramTask CustomBatchTask ',
  'SrcPath': '\\10.13.66.8\\wps\\cases\\wps\\大数据\\排版二梯度8w\\节属性 ',
  'testcaseconfig': 'Configs\\Core\\Wps\\CfgTrunk\\WPS-字符排版-读写\\字符排版-单一读盘.xml'
}

task_doc_1 = {
  'Id': '1020598',
  'CrontabId': '1001983',
  'TaskName': 'Win7 812 WPS{ 双击启动} 2013界面 【Win7】812-WPS{-双击启动}-2013界面',
  'ToolName': 'MemoryMonit',
  'Disabled': 'False',
  'Note': '',
  'Type': 'CustomBatchTask SvnExportTask CopyTask RunProgramTask RunProgramTask CopyTask RunProgramTask CustomBatchTask ',
  'SrcPath': 'E:\\V8AutoTest\\MemoryMonit\\Resource\\Public\\skin\\2013 E:\\V8AutoTest\\MemoryMonit\\Resource\\Public\\skin\\2013 E:\\V8AutoTest\\MemoryMonit\\Results '
}

# prefix前缀查询
# match multi_match
# fuzzy 词级别查询
# search_doc = {'query': {'fuzzy': {'Branch': '用例平台'}}}
# 多字段模糊搜索
search_doc = {
  "query": {
    "multi_match": {
      "fields": ["Name", "Branch", "Edition", "Id", "Note", "Type", "SrcPath", "testcaseconfig"],
      "query": "中文拼写检查",
      "fuzziness": "AUTO"
    }
  }
}

task_search_doc = {
  "query": {
    "multi_match": {
      "fields": ["Id", "CrontabId", "TaskName", "ToolName", "SubscribersMail", "Type", "Path"],
      "query": "MemoryMonit",
      "fuzziness": "AUTO"
    }
  }
}

# 获取数据
# f = open('计划数据模板_替换特定符号.txt', 'r')
# doc = f.read()
# f.close()

# print(doc)

# 默认host为localhost,port为9200.但也可以指定host与port
es = Elasticsearch()
# 添加或更新数据,index，doc_type名称可以自定义，id可以根据需求赋值,body为内容
# es.index(index="pe", doc_type="crontab", id=2, body=doc_1)
# es.index(index="pe", doc_type="task", id=2, body=task_doc_1)
# es.update(index="my_index", doc_type="test_type", id=1, body={"doc": {"name":"java","addr":"惠东"}})

# 录入计划和任务的数据
# f = open('crontab_data.txt', 'r', encoding='utf-8')
# crontab_data = json.loads(f.read())
# f.close()
#
# for i in range(0, len(crontab_data)):
#     data = get_data_crontab(crontab_data[i])
#     if data is not None:
#         es.index(index='pe', doc_type='crontab', id=int(i+1), body=data)
#
# f = open('task_data.txt', 'r', encoding='utf-8')
# task_data = json.loads(f.read())
# f.close()
#
# for i in range(0, len(task_data)):
#     data = get_data_task(task_data[i])
#     if data is not None:
#         es.index(index='pe', doc_type='task', id=int(i+1), body=data)

# 删除
# es.delete(index="pe", doc_type="crontab", id=1)
# es.delete(index="pe", doc_type="crontab", id=2)
# es.delete(index="pe", doc_type="task", id=1)
# es.delete(index="pe", doc_type="task", id=2)

# 批量操作
# result = es.bulk(body=doc, index="my_index", doc_type="test_type")

# 获取索引为pe,文档类型为crontab的所有数据,result为一个字典类型
crontab_result = es.search(index="pe", doc_type="crontab", body=search_doc, filter_path=['hits.hits._*'])
task_result = es.search(index="pe", doc_type="task", body=task_search_doc, filter_path=['hits.hits._*'])

# 打印所有数据
# for item in result["hits"]["hits"]:
#     print(item["_source"])

# 获取插入的数据
# result = es.get(index="pe", doc_type="task", id=100)
# print(result)
print('计划--------------')
for info in crontab_result['hits']['hits']:
    print(info)
print('任务--------------')
for info in task_result['hits']['hits']:
    print(info)