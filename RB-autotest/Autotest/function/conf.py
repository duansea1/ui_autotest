'''
Created on 2017年7月27日

@author: caocheng
'''
import configparser
import os

projname='AutoTest'
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

if __name__=='__main__':
    pass
