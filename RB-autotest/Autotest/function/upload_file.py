'''
# -*- coding: utf-8 -*-
#开发人员:   chnepeng
#开发日期:   2019-06-05
#文件项目:   
#文件名称:   用autoit方法制作的upload.exe上传文件
 '''
import os

def upload_file(file):
    '''
    打开上传窗口后，再执行此方法，即可上传文件
    upload.exe 为执行程序，对文件路径做了参数化
    file 为AutoTest下上传文件的路径  例如  file\b2bpc\Enterprise_qualification.png
    :param file_name:
    :return:
    '''
    a_path = (os.path.abspath (os.path.join (os.getcwd (), "../..")))  # 获取AutoTest目录
    file_path = os.path.join (a_path, r"%s"%file)  # 拼接出导入文件路径
    exe_path = os.path.join (a_path, r"file\b2bpc\upload.exe %s")  # 拼接出upload.exe文件路径
    os.system(exe_path % file_path)  # 对excel文件路径参数化执行exe上传文件)