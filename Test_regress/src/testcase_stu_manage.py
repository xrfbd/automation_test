# -*- coding: UTF-8 -*-

import unittest, ConfigParser, random, time, os, logging, MySQLdb
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import HTMLTestRunner

from PO.base import Base
import login, student_management

class StudentMangeTest(unittest.TestCase):
    
    def setUp(self):

        self.cfg_file = 'config.ini'
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read(self.cfg_file)
        self.browser = self.cfg.get("env_para", "browser")
        self.org_name = self.cfg.get("env_para", "org_name")
        self.org_password = self.cfg.get("env_para", "org_password")
        self.user_name = self.cfg.get("env_para", "user_name")
        self.user_password = self.cfg.get("env_para", "user_password")
        self.base_url = self.cfg.get("env_para", "base_url")
        self.dbhost = self.cfg.get("env_para", "dbhost")

        if os.path.exists("C:\\test_rs_pic") != True:
                os.system("mkdir C:\\test_rs_pic")

        if self.browser == 'ie':
            self.driver = webdriver.Ie()
        elif self.browser == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser == 'Chrome':
            chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver = webdriver.Chrome(chromedriver)
        elif self.browser == "Html":
            self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())
        else:
            self.driver = webdriver.Ie()

        self.driver.implicitly_wait(3)
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        cookie1 = self.cfg.get('env_para', 'cookie1')
        if(cookie1 == 'no'):
            login.login_by_logindo(self.cfg, self.driver, self.base_url, self.org_name, self.org_password)
            self.cfg.set("env_para", "cookie1", str(self.driver.get_cookie('ASUSS')['value']))
            self.cfg.write(open(self.cfg_file, "w"))
           
            #本来还有一个叫RM的cookie，但是值都是rm不变所以不取了
            # path=/; domain=.ablesky.com
        else:
            self.driver.add_cookie({'name':'ASUSS', 'value':cookie1, 'path':'/', 'domain':'.ablesky.com'})
            self.driver.add_cookie({'name':'RM', 'value':'rm'})  

    # @unittest.skip("test")
    #导入一个学员
    def test_import_one_student(self):
        ba = Base(self.driver)
        # stu_name = "exam3996"#还是固定的学员，以后改成注册那生成的学员
        stu_name = self.cfg.get("env_para", "import_name")
        student_management.import_one_student(self.cfg, self.driver, self.base_url, stu_name)
        filename = ba.save_screenshot()
        print "image:"+filename
        #验证
        self.driver.refresh()
        time.sleep(5)
        ts = ba.is_element_present(By.XPATH, "//span[@title=\'"+stu_name+"\']")
        if ts == False:
            rs = False
        else:
            rs = True
        self.assertEqual(True, rs)

    # @unittest.skip("test")
    #导入多个学员
    def test_import_multi_student(self):
        ba = Base(self.driver)
        student_management.import_multi_student(self.cfg, self.driver, self.base_url, r"C:\register_user_list.txt")
        filename = ba.save_screenshot()
        print "image:"+filename

    # @unittest.skip("test")
    #创建学员
    def test_auto_create_student(self):
        ba = Base(self.driver)
        stu_num = 1
        student_management.auto_create_student(self.cfg, self.driver, self.base_url, stu_num)
        filename = ba.save_screenshot()
        print "image:"+filename

    # @unittest.skip("test")
    #给一个学员开通课程
    def test_open_course_for_one(self):
        ba = Base(self.driver)
        student_management.open_course_for_one(self.cfg, self.driver, self.base_url)
        filename = ba.save_screenshot()
        print "image:"+filename

    # @unittest.skip("test")
    #给多个学员开通课程
    def test_open_course_for_multi(self):
        ba = Base(self.driver)
        student_management.open_course_for_multi(self.cfg, self.driver, self.base_url)
        filename = ba.save_screenshot()
        print "image:"+filename

    # @unittest.skip("test")
    #管理学员播放授权数
    def test_manage_course_num(self):
        ba = Base(self.driver)
        student_management.manage_course_num(self.cfg, self.driver, self.base_url, self.user_name)
        filename = ba.save_screenshot()
        print "image:"+filename

    # @unittest.skip("test")
    #购买授权
    def test_buy_open_num(self):
        ba = Base(self.driver)
        student_management.buy_open_num(self.cfg, self.driver, self.base_url)
        filename = ba.save_screenshot()
        print "image:"+filename

    def tearDown(self): #在每个测试方法执行后调用，这个地方做所有清理工作
        self.driver.quit()