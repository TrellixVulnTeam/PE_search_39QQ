import xml.dom.minidom
from pathlib import Path

class CaseResult:
    def __init__(self, case_name, case_url_base, result,
                 before=None, before2=None, before3=None,
                 after=None, after2=None, after3=None):
        self.case_name = case_name
        if not case_url_base.endswith('/'):
            case_url_base = case_url_base + '/'
        self.case_url = case_url_base + self.case_name.replace('\\', '/')
        self.result = result
        self.before = before
        self.before2 = before2
        self.before3 = before3
        self.after = after
        self.after2 = after2
        self.after3 = after3

    def data(self):
        return vars(self)

    def __str__(self):
        return str(self.data())

def filter_file(path, kws):
    for child in Path(path).iterdir():
        if child.is_file() and all(kw.lower() in child.name.lower() for kw in kws):
            return child
    return None

def find_elapsedyimems(components):
    actions = list(components[0].getElementsByTagName('Action'))
    action_len = len(actions) - 1
    for action in actions:
        if action.getAttribute("ElapsedTimeMs"):
            return actions.index(action), action_len + action_len - actions.index(action)

def get_click_lnk_cases(case_url_base, result_dir=None):
    if not result_dir:
        result_dir = r"C:\Users\84481\Desktop\MemoryMonit\Results"

    cases = []
    res_file = filter_file(result_dir, ['_result_', '.xml'])
    print('找到的内存工具结果文件为：' + str(res_file))

    tree = xml.dom.minidom.parse(str(res_file))
    collection = tree.documentElement
    components = list(collection.getElementsByTagName('Component'))
    # 计时属性出现的下标，以及到下一个的跨度
    index, span = find_elapsedyimems(components)
    num = 1
    for component in components:
        actions = list(component.getElementsByTagName('Action'))
        for i in range(index, len(actions), span):
            case_name = 'close' + str(num)
            case = CaseResult(case_name=case_name, case_url_base=case_url_base, result=float(actions[i].getAttribute("ElapsedTimeMs")))
            print(case)
            cases.append(case.data())
            num = num + 1

    return cases, 'ms'

get_click_lnk_cases('emmmmm')