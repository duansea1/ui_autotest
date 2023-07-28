'''
Created on 2018年5月7日

@author: geqiuli
'''

def ope_home(dr):
    ''''''
    #ope_html=dr.page_source
    print(dr.find_element_by_id('btnw').text.strip())
    print('左侧菜单：')
    menus=dr.find_elements_by_css_selector('div.barInner>ul.navigation>li>a')
    for menu in menus:
        print(menu.text.strip())
    

if __name__ == '__main__':
    pass