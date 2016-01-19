# -*- coding: UTF-8 -*-
'''
Created on Dec. 09, 2014

@author: yilulu
'''
import re
import time

import base

class PaymentPage(base.Base):


	def __init__(self, driver, cfg):
		self.dr = driver
		self.cfg = cfg
		self.base_url = cfg.get('env_para', 'base_url')

	def open(self, course_url, ptype="course"):
		"""
		ptype 是购买东西的类型，course 为课程
		                       exampaper 为试卷

		"""
		course_id = re.search(r'\d{1,10}', course_url).group(0)
		host = self.base_url.replace("http://","")
		self.dr.get("%spaymentRedirect.do?action=paymentDomainRedirect&\
			host=%s&grouponid=&type=%s&id=%s"\
			%(self.base_url, host, ptype, str(course_id)))

    #选择账户余额支付
	def choose_balance_pay(self):
		time.sleep(2)
		self.dr.find_element(self.cfg.get('org_index','balance_by'), \
			self.cfg.get('org_index','balance')).click()
			
	def choose_use_rmb(self):
		time.sleep(2)
		self.dr.find_element(self.cfg.get('org_index','use_rmb_by'), \
			self.cfg.get('org_index','use_rmb')).click()

	def click_pay(self):
		time.sleep(3)
		self.dr.find_element(self.cfg.get('org_index', 'pay_ok_by'), \
			self.cfg.get('org_index', 'pay_ok')).click()
		
	def click_look_Coursedetail(self):
		time.sleep(3)
		self.dr.find_element_by_link_text(u"查看课程详情").click()
		time.sleep(3)
		