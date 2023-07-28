'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-05-27
#文件项目:   
#文件名称:   
 '''


def is_number(s) :
    '''
    判断字符串是否为数字
    @author: chenpeng
    :param s:
    :return:
    '''
    try :
        float (s)
        return True
    except ValueError :
        pass

    try :
        import unicodedata
        unicodedata.numeric (s)
        return True
    except (TypeError, ValueError) :
        pass

    return False