'''
Created on 2017年8月7日

@author: geqiuli
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

def switch_handle(driver,*handles,**kw):
    '''切换窗口
    @param handle: 之前的窗口句柄 
    @param *handles: 不定参数，可以添加多个
    @param **kw: handle_list,列表
    '''
    
    for h in driver.window_handles:
        if h not in handles:
            if 'handle_list' in kw:
                if h not in kw['handle_list']:
                    driver.switch_to.window(h)
                    break
            else:
                driver.switch_to.window(h)
                break
                
            
def wait_until_condition(selenium,condition,element,message,timeout=60):    
    '''
    @param condition: 
    @param element: eg:(By.CSS_SELECTOR,'.login_page>div>button')
    
    '''
    if condition=='clickable':
        WebDriverWait(selenium,timeout).until(EC.element_to_be_clickable(),message=message)
    elif condition=='display':
        WebDriverWait(selenium,timeout).until(EC.invisibility_of_element_located(),message=message)
    elif condition=='invisibility':
        WebDriverWait(selenium,timeout).until(EC.invisibility_of_element_located(),message=message)
        
def close_other_windows(selenium,target_window):   
    '''返回指定窗口，并关闭其他所有窗口'''
    all_handles=selenium.window_handles
    if len(all_handles)>1:
        for hand in all_handles:
            if hand!=target_window:
                selenium.switch_to.window(hand)
                sleep(0.5)
                selenium.close()
                sleep(0.5)
                selenium.switch_to.window(target_window)
    sleep(0.5)
        
if __name__ == '__main__':
    pass