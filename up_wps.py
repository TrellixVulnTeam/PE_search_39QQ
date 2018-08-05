import pprint
import argparse
import re
import os

from lib import JobResult, send_and_backup_res
from get_old_perf_cases import get_old_perf_cases
from get_memeory_cases import get_memeory_cases
from get_new_memeory_cases import get_new_memeory_cases
from get_draw_perf_cases import get_draw_perf_cases
from get_sak_perf_cases import get_sak_perf_cases
from get_click_lnk_cases import get_click_lnk_cases

SUPPORTED_TOOLTYPE = [
    '新建内存占用',
    '新建内存峰值',
    '内存占用',
    '内存峰值',
    '老性能启动',
    '老性能打开',
    '老性能保存',
    '老性能关闭',
    '绘制效率',
    'SAK性能',
    '双击启动',
    '关闭性能',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pe_job_id', help='', type=int)
    parser.add_argument('--pe_task_id', help='', type=int)
    parser.add_argument('--case_url_base', help='')
    parser.add_argument('--result_dirs', help='')
    parser.add_argument('--app_name', help='', choices=['WPS', 'ET', 'WPP', 'WORD', 'EXCEL', 'PPT'])
    parser.add_argument('--task_name', help='')
    # parser.add_argument('--task_measurement', help='')
    parser.add_argument('--product_name', help='')
    parser.add_argument('--fire_user_name', help='')
    parser.add_argument('--description', help='')
    parser.add_argument('--tool_types', help='多个可用中文分号分隔')
    return parser.parse_args()


def upload_job(cases, args):
    job = JobResult(cases=cases, **args)
    send_and_backup_res(job)
    return job


def clean_notes(s):
    s = s.replace('(SAKPerf)', '') \
        .replace('(KSOPerformanceV3)', '')\
        .replace('(DrawPerformance)', '')\
        .replace('(MemoryMonit)', '') \

    return re.sub("[\{].*?[\}]", "", s)


def save_args(arg_dic):
    line = r'"C:\ProgramData\Anaconda3\python.exe" up_wps.py'
    for k, v in arg_dic.items():
        line += ' --' + str(k) + ' ' + str(v)
    print('up_wps.py args is ' + '\n' + line)
    bk = os.path.join(BASE_DIR, 'LastRun.bat')
    f = open(bk, 'w')
    f.write(line + '\n')
    f.write('pause' + '\n')
    f.close()


if __name__ == '__main__':
    args = vars(get_args())
    save_args(args)

    case_url_base = args.pop('case_url_base')
    tool_types = re.split(r"；|;", args.pop('tool_types'))
    result_dirs = re.split(r"；|;", args.pop('result_dirs'))

    cases = None
    for tool_type, result_dir in zip(tool_types, result_dirs):
        if tool_type in ['新建内存占用', '新建内存峰值', ]:
            cases, task_measurement = get_new_memeory_cases(tool_type, case_url_base, result_dir)
        elif tool_type in ['内存占用', '内存峰值', ]:
            cases, task_measurement = get_memeory_cases(tool_type, case_url_base, result_dir)
        elif tool_type in ['老性能启动', '老性能打开', '老性能保存', '老性能关闭', ]:
            cases, task_measurement = get_old_perf_cases(tool_type, case_url_base, result_dir)
        elif tool_type in ['绘制效率', ]:
            cases, task_measurement = get_draw_perf_cases(case_url_base, result_dir)
        elif tool_type in ['SAK性能', ]:
            cases, task_measurement = get_sak_perf_cases(case_url_base, result_dir)
        elif tool_type in ['双击启动', ]:
            cases, task_measurement = get_click_lnk_cases(case_url_base, result_dir)
        elif tool_type in ['关闭性能', ]:
            cases, task_measurement = get_click_lnk_cases(case_url_base, result_dir)
        else:
            print('tool_types参数{}错误，已跳过'.format(tool_type))    # xp下不能用 f string
            continue

        original_task_name = args['task_name']
        args['task_name'] = clean_notes(original_task_name) + '-' + tool_type
        args['task_measurement'] = task_measurement
        job = upload_job(cases, args)
        args['task_name'] = original_task_name
        args.pop('task_measurement')
    print('所有合法结果都上传成功')
