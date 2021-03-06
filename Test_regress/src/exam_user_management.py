# -*- coding: UTF-8 -*-
'''
Created on Jul 24, 2014

@author: yilulu
'''

import time

from PO.exam_user_page import UserpaperListPage, UserexampaperPage
from PO.payment_page import PaymentPage

def buy_paper(cfg, driver, paper_url):
    pay = PaymentPage(driver, cfg)
    pay.open(paper_url, "exampaper")
#    pay.self_dr_refresh()
    exm = pay.choose_buyNow()
    pay.save_screenshot()
    if exm == 0:
        pay.choose_balance_pay()
        pay.choose_use_rmb()
        pay.click_pay()
        pay.click_look_Examdetail()
    else:
        pass

#学员考试
def exam_user(cfg, driver, base_url, operation, blank_pager, question_answer, paper_name):
    userpaperlist = UserpaperListPage(driver, cfg)
    userpaperlist.enter_exampaperlist()
    userpaperlist.enter_practice()
    userpaperlist.save_screenshot()
    userpaperlist.click_examnow()
    userpaperlist.save_screenshot()
    userpaperlist.click_paper()
    userpaperlist.save_screenshot()
    userexampaper = UserexampaperPage(driver, cfg)
#    exam_time = userexampaper.get_examtime()
#    userpaperlist.save_screenshot()
#    userexampaper.click_startexam()
    question_title = userexampaper.get_questiontitle()
    time.sleep(5)
     # blank_pager=1 是白卷 ;blank_pager=0 是做了一个题
    if blank_pager == 0:
        #单选 多选
        if question_title == u"单选题" or question_title == u"多选题":
            try:
                userexampaper.click_selectquestion()
            except:
                None     
        #是非题
        elif question_title == u"是非题":
            try: 
                userexampaper.click_yesnoquestion() 
            except:
                None      
        #填空题
        elif question_title == u"填空题":
            try: 
                userexampaper.click_blankquestion(question_answer)  
            except:
                None  
        #问答题  
        elif question_title == u"问答题": 
            try:        
                userexampaper.click_essayquestion(question_answer)  
            except:
                None 
        #完形填空题
        elif question_title == u"完形填空题":
            try:
                userexampaper.click_clozequestion()
            except:
                None 
        #综合题
        elif question_title == u"综合题":
            #第一个是单选 or 多选
            try:
                userexampaper.click_all_selectquestion()
            except:
                None
            #是非
            try:
                userexampaper.click_all_yesnoquestion()
            except:
                None
            #填空
            try:
                userexampaper.click_all_blankquestion(question_answer)
            except:  
                None
            #问答
            try:
                userexampaper.click_all_essayquestion(question_answer)
            except:
                None
        ###综合题结束
        #等于0是自动提交
        time.sleep(2)
        if operation == '0':
             time.sleep(exam_time * 60 + 2)
        try:        
            userexampaper.click_submit()
            userexampaper.click_continueexam()
            userexampaper.click_submit()
            userexampaper.click_confirmsubmit()
        except:
             None
    #学员提交白卷
    else:
        time.sleep(2)
        if operation == '0':
             time.sleep(exam_time * 60 + 2)
        try:   
            userexampaper.click_submit()
            userexampaper.click_continueexam()
            userexampaper.click_submit()
            userexampaper.click_confirmsubmit()
        except:
             None
    