# -*- coding: UTF-8 -*-
'''
Created on 2014-12-20

@author: guoyuling
'''
import time

from selenium.webdriver.support.wait import WebDriverWait

import base
from myoffice_page import MyOfficePage

class ExamCateListPage(base.Base):


    def __init__(self, driver, cfg):
        self.dr = driver
        self.cfg = cfg
        self.base_url = cfg.get('env_para', 'base_url')

    #填写类目名称
    def input_cname(self, cate_name):
        time.sleep(1)
        c_input = self.dr.find_element(self.cfg.get('exam', 'cate_addname_by'), \
            self.cfg.get('exam', 'cate_addname'))
        c_input.clear()
        c_input.send_keys(cate_name)
        
    #填写类目描述
    def input_cdetail(self, cate_detail):
        cd_input = self.dr.find_element(self.cfg.get('exam', 'cate_desname_by'), \
            self.cfg.get('exam', 'cate_desname'))
        cd_input.clear()
        cd_input.send_keys(cate_detail)

    #新增类目
    def click_create(self):
        time.sleep(1)
        self.dr.find_element(self.cfg.get('exam', 'cate_newcateid_by'), \
            self.cfg.get('exam', 'cate_newcateid')).click()        

    #编辑类目
    def click_modify_cate(self):
        time.sleep(1)
        self.dr.find_elements(self.cfg.get('exam', 'cate_mod_by'), \
            self.cfg.get('exam','cate_mod'))[0].click()  

    #删除类目
    def click_delete_cate(self):
        time.sleep(1)
        self.dr.find_elements(self.cfg.get('exam', 'cate_del_by'), \
            self.cfg.get('exam', 'cate_del'))[-1].click()
        
    #确认新建类目
    def click_addcate_ok(self):
        self.dr.find_element(self.cfg.get('exam', 'cate_oknew_button_by'),\
            self.cfg.get('exam', 'cate_oknew_button')).click()
    
    #确认删除类目
    def click_delcate_ok(self):
        time.sleep(1)
        self.dr.find_element(self.cfg.get('exam', 'cate_oknew_button_by'), \
            self.cfg.get('exam', 'cate_oknew_button')).click()
        