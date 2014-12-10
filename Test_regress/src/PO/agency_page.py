# -*- coding: UTF-8 -*-
'''
Created on Dec. 05, 2014

@author: yilulu
'''
import time
import re
from selenium.common.exceptions import NoSuchElementException

import base
from myoffice_page import MyOfficePage

class CourseAgencyPage(base.Base):


	def __init__(self, driver, cfg):
		self.dr = driver
		self.cfg = cfg
		self.base_url = cfg.get('env_para', 'base_url')

	def open(self):
		m = MyOfficePage(self.dr, self.cfg)
		m.open()
		m.click_myapplyagency()

	def click_manage_course(self):
		try:
			self.dr.find_element_by_link_text(u"管理课程").click()
		except NoSuchElementException, e:
			print u"该机构还没有申请代理"

	def click_edit(self):
		try:
			bh = self.dr.window_handles
			self.dr.find_element_by_link_text(u"编辑").click()
			self.switch_window(bh)
		except NoSuchElementException, e:
			print u"该机构还没有代理课程"


class AgentCourseInputPage(base.Base):

	def __init__(self, driver, cfg):
		self.dr = driver
		self.cfg = cfg
		self.base_url = cfg.get('env_para', 'base_url')

	def input_title(self, title):
		tinput = self.dr.find_element(self.cfg.get('courseRedirect', 'agency_title_by'), \
			self.cfg.get('courseRedirect', 'agency_title'))
		tinput.clear()
		tinput.send_keys(title)

	def input_price(self, price):
		"""
		代理课程的价格是规定的，根据页面上的提示取
		"""
		pinput = self.dr.find_element(self.cfg.get('courseRedirect', 'agency_price_by'), \
			self.cfg.get('courseRedirect', 'agency_price'))
		pinput.clear()
		pinput.send_keys(price)

	def input_rank(self, rank):
		rinput = self.dr.find_element(self.cfg.get('courseRedirect', 'agency_rank_by'), \
			self.cfg.get('courseRedirect', 'agency_rank'))
		rinput.clear()
		rinput.send_keys(rank)

	def click_save(self):
		self.dr.find_element(self.cfg.get('courseRedirect', 'finish_btn_by'), \
			self.cfg.get('courseRedirect', 'finish_btn')).click()
		time.sleep(1)
