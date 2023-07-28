
import configparser
import json
import csv
import os

projname='SupplyChain'
root_dir=os.path.abspath('conftest.py').split(projname)[0]+projname+os.sep
print(root_dir)


cf = configparser.ConfigParser()

def get_system_path():
    tmp = os.path.abspath('').split(projname)
    path = tmp[0] + projname
    return path


def get_system_value(class_name, key):
    tmp = os.path.abspath('').split(projname)
    path = tmp[0]
    if(len(tmp) != 1):
        path += projname
    #print(u'conf路径：'+path)
    path = path + '\conf\system.conf'
    cf.read(path, 'utf-8')
    return cf.get(class_name, key)


def get_local_value(class_name, key):
    fpath=root_dir + os.sep+'conf'+ os.sep + "local.conf"
    cf.read(fpath,'utf-8')
    return cf.get(class_name, key)

def read_txt(file_name, subdir=None):
    if subdir:
        fpath=root_dir + os.sep+'file'+ os.sep + file_name + ".txt"
    else:
        fpath=root_dir + os.sep+'file'+ os.sep + subdir + os.sep + file_name + ".txt"
    arr = []
    with open(fpath, mode='r', encoding='UTF-8') as f:
        for line in f.readlines():
            arr.append(line.strip())
    return arr

def read_json(file_name, source='pc'):
    fpath=root_dir + os.sep+'file'+ os.sep + source + os.sep + file_name + ".json"
    with open(fpath, 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    return listCookies

def read_csv(file_name, source='pc'):
    fpath = root_dir + os.sep+'file'+ os.sep + source + os.sep + file_name + '.csv'
    arr=[]
    with open(fpath,'r', encoding='UTF-8') as f:
        reader=csv.DictReader(f)
        for row in reader:
            arr.append(row)
    return arr

def write_txt(file_name, content, source='pc'):
    '''写入文本内容
    @param file_name: 文件名
    @param content: 要写入的内容，目前支持字符串和列表
    '''
    fpath = root_dir + os.sep+'file'+ os.sep + source + os.sep + file_name + '.txt'
    if isinstance(content, str):
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    elif isinstance(content, list):
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
    
def add_to_txt(file_name, content, source='pc'):
    '''追加到文本内容
    @param file_name: 文件名
    @param content: 要写入的内容，目前支持字符串和列表
    '''
    fpath = root_dir + os.sep+'file'+ os.sep + source + os.sep + file_name + '.txt'
    if isinstance(content, str):
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(content+'\n')
    elif isinstance(content, list):
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write('\n'.join(content))

def write_json(file_name, content, source='pc'):
    fpath=root_dir + os.sep+'file'+ os.sep + source + os.sep + file_name + ".json"
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content))


def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()
    
if __name__=='__main__':
    print(read_csv('querysellerorders', 'yaoex'))
    