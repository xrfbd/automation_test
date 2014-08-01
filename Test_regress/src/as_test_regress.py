# -*- coding: UTF-8 -*-
'''
Created on Sep. 24, 2012

@author: yilulu
'''
import unittest,ConfigParser,random,time,os,MySQLdb
from selenium import webdriver
import login, new_course_management, course_management, student_management, card_management,cate_management,admin_management,user_management,exam_paper, exam_questions,exam_cate_management
import exam_user_management
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class Test(unittest.TestCase):


    def setUp(self):
        
        self.browser = "Chrome"
        self.test_enviroment = "beta"  
        self.org_name = "adm_guo"
        self.org_password = "1234aa"
        self.user_name = "wudingzhiying"
        self.user_password = "1234"
        self.dbhost = "192.168.120.201" #alpha数据库地址：192.168.150.7、beta: 192.168.120.201 omega数据库：192.168.190.74 beta数据库192.168.3.50 gamma: 192.168.120.110r
        #self.independent_url = "www.dlym.com"#独立域名网址
        self.import_name = "sun122"
        self.username = "sun123"
        
        cfg_file = 'config.ini'
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read(cfg_file)
        self.verificationErrors = []
        
        self.total = 0
        
        if self.browser == 'ie':      
            self.driver = webdriver.Ie()
        elif self.browser == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser == 'Chrome':
            chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver =  webdriver.Chrome(chromedriver)
        elif self.browser == "Html":
            self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())
        else:
            self.driver = webdriver.Ie()

        self.driver.implicitly_wait(5)
        self.base_url = "http://www."+self.test_enviroment+".ablesky.com/"
        #self.base_url = "http://www.zhongyan.com/"
        #self.base_url = "http://web1mb1.bp1.ablesky.com/"
        
        if os.path.exists("C:\\test_rs_pic")!= True:
            os.system("mkdir C:\\test_rs_pic")
    
    def connect_db(self,database):
        try:
            conn = MySQLdb.connect(host=self.dbhost, user='root',passwd='mysqlpwd1',db=database,charset='utf8')
        except Exception,e:
            print e
        return conn
    
    def verify_convert(self,course_title,msg):
        
        db='ajaxableskydb'
        conn = self.connect_db(db)
        sql = "SELECT id From course where title=\'"+course_title+"\'"
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        id =  results[0][0]
        print id
        convert_sql ="SELECT convert_status FROM coursecontent where course_id="+str(id)
        cursor.execute(convert_sql)
        convert_results = cursor.fetchall()
        
        for status in convert_results:
            if status[0] != u"done":
                self.verificationErrors.append(msg)
                return False
        else:
            return True
    
    def register(self):#注册改啦要改
        
        self.total += 1
        user_name = ""
        try:
            user_name = login.auto_register(self.cfg, self.driver, self.base_url, 2, 1)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to register!")
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/1_register.png')
          
        self.import_name = user_name #待单个导入学员使用
    
    def login_from_index(self):
        
        self.total += 1
        try:
            login.login_by_as(self.cfg, self.driver, self.base_url, self.org_name, self.org_password)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/1_login.png')
    
    def login_user(self):
        
        try:
            login.login_by_logindo(self.cfg, self.driver, self.base_url, self.user_name, self.user_password)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/1_login_user.png')
    
    def release_normal(self):
        
        self.total += 1
        #file=r"W:\Testing\Testing Files\Automation_test\OLAY.mpe.asc.flv"
        rand_name = str(random.randint(1000,9999))
        title =u"course"+rand_name#在标题中加入随机数字确保课件标题的唯一性
        try:
            new_course_management.course_redirect(self.cfg, self.driver, self.base_url, course_title=title, course_price=10)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/2_normal_course.png')
            
        self.normal_course = title#待用-在数据库中查是否转换失败
        
        
        try:
            rs = self.verify_course(title)
            self.assertEqual(True, rs,"fail to release course!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
            
        #取链接待后面购买
        course_href = self.driver.execute_script("return $(\"a:contains(\'"+title+"\')\").attr('href')")
        self.course_href = self.base_url+course_href

    
    def release_three_video(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"course-three"+rand_name
        try:
            new_course_management.course_redirect(self.cfg, self.driver, self.base_url, ctype=1, isthree=1, course_title=title, course_price=10)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/4_three_video.png')
        
        self.three_title = title   
        
        try:
            rs = self.verify_course(title)
            self.assertEqual(True, rs, "fail to release tree video course!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
        
        #取链接待后面购买
        course_href = self.driver.execute_script("return $(\"a:contains(\'"+title+"\')\").attr('href')")
        self.course_href_2 = self.base_url + course_href
            

            
#现在不好判断是不是双视频了           
    def release_two_video(self):
        
        self.total += 1
        v_file = r"W:\Testing\Testing Files\Automation_test\OLAY.mpe.asc.flv"
        p_file = r"W:\Testing\Testing Files\Automation_test\think.mpeg.asc.flv"
        rand_name = str(random.randint(1000,9999))
        title = u"自动化测试-双视频"+rand_name
        try:
            course_management.release_three_video(self.cfg, self.driver, self.base_url, self.org_name, video_file = v_file, pdf_file = p_file, course_title=title)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/5_two_video.png')
        
        self.two_title = title   
        
        try:
            rs = self.verify_course(title)
            self.assertEqual(True, rs, "fail to release two video course!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
               
    def package_course(self):
        #打包课程，即网络班
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = "onlineclass" + rand_name
        try:
            new_course_management.class_redirect(self.cfg, self.driver, self.base_url, classname=title)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/6_package.png')
        self.package_title = title   
        rs = self.verify_onlineclass(title)
        try:
            self.assertEqual(True, rs)
        except AssertionError,e:
            self.verificationErrors.append(str(e))

        
    def add_cate(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        cate_name = u"catetest"+rand_name
        try:
            cate_management.add_cate(self.cfg, self.driver, self.base_url, self.org_name, cate_name=cate_name)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/7_add_cate.png')
        
        self.driver.implicitly_wait(1)
        actul = self.driver.execute_script("return $(\".categTitleFalse :last\").text()")#取最后一个类目的名称
        try:
            self.assertEqual(cate_name, actul,"the categroy does not exist!")#若最后一个类目名称与新建类目的名称相等则证明新建类目成功
        except AssertionError,e:
            self.verificationErrors.append(str(e))
           
    def presale_course(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = "presaleclass" + rand_name
        try:
            new_course_management.class_redirect(self.cfg, self.driver, self.base_url, classname=title, ctype=2)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/8_presale.png')
            
        self.presale_title = title   
        rs = self.verify_onlineclass(title)
        try:
            self.assertEqual(True, rs,"fail to release presale course!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
              
    def agency_course(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"agencycourse"+rand_name
        try:
            new_course_management.release_agency_course(self.cfg, self.driver, self.base_url, course_title=title)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/9_agency_course.png')
        
        
        try:
            rs = self.verify_course(title)
            self.assertEqual(True, rs,"fail to release agency course!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
    #充值卡 
    def prepaid_cardgroup(self):#充值卡
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"prepaidcard"+rand_name
        price = 100
        #建卡组
        try:
            card_management.add_prepaid_cardgroup(self.cfg, self.driver, self.base_url, self.org_name, group_name=title, group_price=price)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/9_prepaid_cardgroup.png')
        
        self.driver.implicitly_wait(2)
        rs = self.is_element_present(By.LINK_TEXT, title)
        try:
            self.assertEqual(True, rs,"fail to create prepaid cardgroup!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
        #建卡,取考号密码
        card_info=self.add_and_get_card()
        self.p_card_num = card_info[0]
        self.p_card_pwd = card_info[1]
        print self.p_card_num
        print self.p_card_pwd
        #考号
    #添加卡组-充课卡   
    def course_cardgroup(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"coursecard"+rand_name
        
        try:
            card_management.add_course_cardgroup(self.cfg, self.driver, self.base_url, self.org_name, group_name=title)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/10_course_cardgroup.png")
        
        self.driver.implicitly_wait(2)
        rs = self.is_element_present(By.LINK_TEXT, title)
        try:
            self.assertEqual(True, rs,"fail to create course cardgroup!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
        #建卡,取考号密码
        card_info=self.add_and_get_card(1)#充课卡需要传参数
        self.c_card_num = card_info[0]
        self.c_card_pwd = card_info[1]
        # print card_info
     #添加卡组-补课卡         
    def cate_cardgroup(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"catecard"+rand_name
        
        try:
            card_management.add_cate_cardgroup(self.cfg, self.driver, self.base_url, self.org_name, title)
        except Exception,e:
            print e
            self.verificationErrors.append('fail to create course cardgroup!')
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/11_cate_cardgroup.png")
        
        self.driver.implicitly_wait(2)
        rs = self.is_element_present(By.LINK_TEXT, title)
        try:
            self.assertEqual(True, rs,"fail to create cate cardgroup!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
        #建卡,取考号密码
        card_info=self.add_and_get_card()
        self.ca_card_num = card_info[0]
        self.ca_card_pwd = card_info[1]
    #购买试听卡
    def buy_listen_card(self):
        self.total += 1
        try:
            card_management.buy_listen_card(self.cfg, self.driver, self.base_url)
        except Exception,e:
            print e
            self.verificationErrors.append('fail to bug listen card!')
        finally:
            self.driver.save_screenshot("D:/test_rs_pic/buy_listen_card.png")
    #添加试听卡组
    def listen_cardgroup(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"listencard"+rand_name
        
        try:
            card_management.add_listen_cardgroup(self.cfg, self.driver, self.base_url, self.org_name, group_name=title)
        except Exception,e:
            print e
        finally:
            self.driver.save_screenshot("D:/test_rs_pic/12_listen_cardgroup.png")  
        self.driver.implicitly_wait(2)
        rs = self.is_element_present(By.LINK_TEXT, title)
        try:
            self.assertEqual(True, rs,"fail to create listen cardgroup!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
        #建卡,取考号密码
        card_info=self.add_and_get_card()
        self.l_card_num = card_info[0]
        self.l_card_pwd = card_info[1]
        print self.l_card_num
        #######
        
    def add_and_get_card(self, card_type=0):#添加卡并返回第一个卡号和密码
        
        self.total += 1
        try:
            card_management.add_card(self.cfg, self.driver, self.base_url, self.org_name)
            self.driver.implicitly_wait(2)
            if card_type == 0:
                time.sleep(2)
                self.driver.find_element_by_link_text(u"浏览卡").click()
                time.sleep(2)
                card_num = self.driver.execute_script("return $(\"input[name='groupCheck']:eq(0)\").parent().next().text()")
                time.sleep(2)
                card_pwd = self.driver.execute_script("return $(\".textaligncenter\:eq(4)\").text()")
                time.sleep(2) 
            else:
                time.sleep(2)                
                self.driver.find_element_by_css_selector("span.greenbtn35_text").click()
                time.sleep(2)
                card_num = self.driver.execute_script("return $(\"input[type='checkbox']:eq(1)\").parent().text()")
                time.sleep(2)
                #print 'card_num:',card_num
                card_pwd = self.driver.execute_script("return $(\"input[type='checkbox']:eq(1)\").parent().parent().next().children().text()") 
                time.sleep(2)
                #print 'card_pwd', card_pwd        
        except Exception,e:
            print e
            card_num = 0#确保有返回值不会报错
            card_pwd = 0
            
        return card_num,card_pwd
    
    #添加考试卡并返回第一个卡号
    def add_exam_card(self):
        self.total += 1
        count = 5
        try:
            self.page_catename = card_management.get_academy_catename(self.cfg, self.driver, self.base_url)
            exam_paper.create_paper(self.cfg, self.driver, self.base_url, self.page_catename, 1, 1, 1, 1)
            self.examcard_num = card_management.add_exam_card(self.cfg, self.driver, self.base_url,count)
            #self.examcard_num = card_management.add_exam_card(self.cfg, self.driver, self.base_url)
        except Exception,e:
            print e
            self.verificationErrors.append('fail to add exam card!')
        finally:
            self.driver.save_screenshot("D:/test_rs_pic/add_exam_card.png")
    #使用考试卡
    def use_exam_card(self):
        self.total += 1
        #examcard_num = self.add_exam_card()
        #self.login_user()
        try:
            card_management.user_usexamcard(self.cfg, self.driver, self.base_url,self.examcard_num)
        except Exception,e:
            print e
            self.verificationErrors.append('fail to use exam card!')
        finally: 
            self.driver.save_screenshot("D:/test_rs_pic/user_exam_card.png") 
            
    
    def delete_cate(self):
    
        self.total += 1
        try:
            before_delete = cate_management.delete_cate(self.cfg, self.driver, self.base_url, self.org_name)
            #print before_delete
        except Exception,e:
            print e
            before_delete ="0"
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/12_delete_cate.png")           
        self.driver.implicitly_wait(1)
        after_delete = self.driver.execute_script("return $(\".categTitle:last\").text()")#取最后一个类目的名称
        print after_delete
  
        try:
            rs = (before_delete == after_delete )
            self.assertEqual(True, rs,"fail to delete category!")#若删除前后最后一个类目名类不同则证明删除类目成功
        except AssertionError,e:
            self.verificationErrors.append(str(e))
            
    def add_course_to_cate(self):
        
        self.total += 1
        try:
            course_name = cate_management.add_courese_to_cate(self.cfg, self.driver, self.base_url, self.org_name)
            actual_name = self.driver.execute_script("return $(\"input[name='course_ckeckbox']:eq(0)\").next().text()")
            actual_name = actual_name.strip()   
            print course_name,actual_name
        except Exception,e:
            print e
            self.verificationErrors.append('fail to add course to category!') 
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/13_add_course_to_cate.png")
            
        try:      
            self.assertEqual(course_name, actual_name, "fail to add course to category!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))   
     
    
            
    def import_one_student(self):
        
        self.total += 1
        #单个导入学员
        try:
            student_management.import_one_student(self.cfg, self.driver, self.base_url, self.org_name, self.import_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to import one student!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/import_one_student.png")
        
        #验证
        self.driver.refresh()
        rs = self.is_element_present(By.XPATH, "//span[@title=\'"+self.import_name+"\']")
        try:
            self.assertEqual(True, rs, "fail to import one student!")
        except AssertionError,e:
            self.verificationErrors.append(str(e))
            
    def import_multi_student(self):
        
        self.total += 1
        try:
            student_management.import_multi_student(self.cfg, self.driver, self.base_url, self.org_name, r"C:\register_user_list.txt")
        except Exception,e:
            print e
            self.verificationErrors.append("fail to import multi student!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/import_multi_student.png")
            
        #验证,待完成
    def create_multi_student(self):
        
        self.total += 1
        stu_num = 5
        try:
            student_management.auto_create_student(self.cfg, self.driver, self.base_url, self.org_name, stu_num)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to create multi student!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/create_student.png")
            
        #验证，待完成
      
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True 
    
    def verify_course(self,title): #去知识库检查是否存在
        
        self.driver.find_element_by_link_text(u"课程中心").click()
        self.driver.implicitly_wait(2) 
        rs = self.is_element_present(By.LINK_TEXT, title)
        return rs

    def verify_onlineclass(self, classname):
        self.driver.implicitly_wait(1) 
        rs = self.is_element_present(By.LINK_TEXT, classname)
        return rs
    #充值卡
    def use_prepaidcard(self):

        self.total += 1
        try:
            confirm_num = card_management.use_prepaid_card(self.cfg, self.driver, self.base_url, self.p_card_num, self.p_card_pwd)
            #验证
            if self.p_card_num != confirm_num :
              self.verificationErrors.append('fail to use prepaid card!')  
        except Exception,e:
            print e
            self.verificationErrors.append('fail to use prepaid card!')
        finally: 
            self.driver.save_screenshot("C:/test_rs_pic/use_prepaidcard.png")
    
    def use_coursecard(self):#充课卡
        self.total += 1
        try:
            confirm_num = card_management.use_prepaid_card(self.cfg, self.driver, self.base_url, self.c_card_num, self.c_card_pwd)
            #验证
            if self.c_card_num != confirm_num :
               self.verificationErrors.append('fail to use course card!')             
        except Exception,e:
            print e
            self.verificationErrors.append('fail to use course card!')
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/use_coursecard.png")
            
        #验证,待完成
    
    def use_catecard(self):#补课卡
        
        self.total += 1
        try:
            course_num = card_management.use_course_card(self.cfg, self.driver, self.base_url, self.ca_card_num, self.ca_card_pwd)
            #验证
            if self.ca_card_num != course_num :
              self.verificationErrors.append('fail to use category card!')  
        except Exception,e:
            print e
            self.verificationErrors.append('fail to use category card!')
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/use_catecard.png")
                    
    def use_listencard(self):#试听卡
        
        self.total += 1
        try:
            login.login_by_logindo(self.cfg, self.driver, self.base_url, self.l_card_num, self.l_card_pwd)
        except Exception,e:
            print e
            self.verificationErrors.append('fail to use listen card!')
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/use_listencard.png")
                               
    
    def add_admin(self):
        
        self.total += 1
        try:
            admin_info = admin_management.auto_create_admin(self.cfg, self.driver, self.base_url, self.org_name, adm_num=2)
            #验证
            for admin in admin_info:
                xpath = "//div[text()=\'"+admin+"\']"
                self.driver.implicitly_wait(2)
                rs = self.is_element_present(By.XPATH, xpath)
                if rs == False:
                    self.verificationErrors.append("fail to create admin!")
        except Exception,e:
            print e
            self.verificationErrors.append("fail to create admin!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/add_admin.png")
        

                
    def modify_admin(self):
        
        self.total += 1
        admin_name = ""
        try:
            admin_name = admin_management.modify_admin(self.cfg, self.driver, self.base_url)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to modify admin!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/modify_admin.png")
            
        #验证
        xpath = "//div[text()=\'"+admin_name+"\']"
        self.driver.implicitly_wait(2)
        rs = self.is_element_present(By.XPATH, xpath)
        if rs == False:
            self.verificationErrors.append("fail to modify admin!")
            
    def delete_admin(self):
        
        self.total += 1
        #before_num = self.driver.execute_script("return $(\"a[]\")")
        #print before_num
        try:
            admin_management.delete_admin(self.cfg, self.driver, self.base_url)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to delete admin!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/delete_admin.png")
            
        #验证
        
    

    def release_announcement(self):
        
        self.total += 1
        rand_name = str(random.randint(1000,9999))
        title = u"自动化公告"+rand_name
        try:
            title = user_management.release_announcement(self.cfg, self.driver, self.base_url, self.org_name, title)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to release announcement!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/release_announcement.png")  
            
    def release_href_course(self):
        
        self.total += 1
        try:
            user_management.release_href_course(self.cfg, self.driver, self.base_url, self.org_name) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to use link")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/user_management_link.png")
        
            
    def verify_all_course_convert(self):
        self.verify_convert(self.normal_course,"fail to convert normal course!")
        self.verify_convert(self.three_title, "fail to convert three video course!")
        #self.verify_convert(self.two_title, "fail to convert three video course!")
        #self.verify_convert(self.space_course, "fail to convert course from space!")
    
    def buy_course_use_RMB(self):
        
        self.total += 1
        try:
            user_management.buy_course(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to buy course use rmb!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/href_course.png")
        #验证待完成
        
    def buy_course_use_card(self):
        
        self.total += 1
        try:
            user_management.buy_course_usecard(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to buy course use card!")
            
    def open_course_for_one(self):
        
        self.total += 1
        try:
            student_management.open_course_for_one(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to open course for one!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/open_course_for_one.png")
            
        #验证，待完成
        
    def open_course_for_multi(self):
        
        self.total += 1
        try:
            student_management.open_course_for_multi(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to open course for multi!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/open_course_for_multi.png")
            
        #验证，待完成
    
    def add_playnum(self):  
       
        self.total += 1
        try:
            student_management.add_playnum(self.cfg, self.driver, self.base_url, self.org_name)  
        except Exception,e:
            print e
            self.verificationErrors.append("fail to add playnum!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/add_playnum.png")
            
        #验证，待完成
        
    def buy_open_num(self):
        
        self.total += 1
        bnum = 2
        try:
            student_management.buy_open_num(self.cfg, self.driver, self.base_url, self.org_name,bnum)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to buy open num!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/buy_open_num.png")
    
    def change_headpic(self):
        
        self.total += 1
        try:
            user_management.org_chang_headpic(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to change headpic!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/change_headpic.png")
            
        #验证
    def change_homelogo(self):
        
        self.total += 1
        try:
            user_management.change_homelogo(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to change homelogo!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/change_homelogo.png")   
                 
    def change_banner(self):
        
        self.total += 1
        try:
            user_management.change_banner(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to change banner!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/change_banner.png")
        
        #验证
    
    def modify_pagefoot(self):
       
        #self.total += 1
        #foot_info = '12'
        #foot_icp = '12'
        try:
            user_management.modify_pagefoot(self.cfg, self.driver, self.base_url, self.org_name) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to modify_pagefoot")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/modify_pagefoot.png")
    
    def login_from_independent_domian(self):
        
        try:
            login.logout_by_independent_domian(self.driver, self.independent_url)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to login from independent_domian!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/login_from_independent_domian.png")
            
        #验证
            
    def logout_from_independent_domian(self):
        
        try:
            login.logout_by_independent_domian(self.driver, self.independent_url)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to logout from independent domian!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/logout_from_independent_domian.png")
        
        #验证
        
    def add_photot(self):
        
        pic = r"W:\Testing\Testing Files\Automation_test\pic.jpg"
        pic_num=5
        try:
            user_management.auto_add_photo(self.cfg, self.driver, self.base_url, self.user_name, pic, pic_num)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to add photo!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/add_photot.png")
            
       #验证
    def add_exam_subject(self):#新建考试科目
        
        self.total += 1
        try:
            subject_info = exam_cate_management.auto_create_subject(self.cfg, self.driver, self.base_url, self.org_name, sub_num=2)
        
            #验证
            for subject in subject_info:
                xpath = "//div[text()=\'"+subject+"\']"
                self.driver.implicitly_wait(2)
                rs = self.is_element_present(By.XPATH, xpath)
                if rs == False:
                    self.verificationErrors.append("fail to create subject!")
                    
        except Exception,e:
            print e
            self.verificationErrors.append("fail to create subject!")
        finally:
            self.driver.save_screenshot("D:/test_rs_pic/add_subject.png")
            
            
            
    def modify_exam_subject(self):#编辑科目
        
        self.total += 1
        try:
            subject_name = exam_cate_management.modify_subject(self.cfg,self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to modify subject!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/modify_subject.png")
            
        #验证
        
        
    def delete_exam_subject(self):#删除科目
        
        self.total += 1
        try:
            exam_cate_management.delete_subject(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to delete subject!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/delete_subject.png")
            
    def create_exam_cate(self):#新建类目
        self.total += 1
        try:
            cate_info = exam_cate_management.auto_create_exam_cate(self.cfg, self.driver, self.base_url, self.org_name, cate_num=1)
        
            #验证
            for cate in cate_info:
                xpath = "//div[text()=\'"+cate+"\']"
                self.driver.implicitly_wait(2)
                rs = self.is_element_present(By.XPATH, xpath)
                if rs == False:
                    self.verificationErrors.append("fail to create cate!")
                    
        except Exception,e:
            print e
            self.verificationErrors.append("fail to create cate!")
        finally:
            self.driver.save_screenshot("D:/test_rs_pic/add_cate.png")



    def modify_exam_cate(self):#编辑类目
        
        self.total += 1
        try:
            exam_cate_management.modify_exam_cate(self.cfg,self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to modify cate!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/modify_cate.png")
            
        self.driver.implicitly_wait(2)       
        
        
    def delete_exam_cate(self):#删除类目
        self.total += 1
        try:
            exam_cate_management.delete_exam_cate(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to delete cate!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/delete_cate.png")
            
    def add_exam_point(self):#新建考点
        self.total += 1
        try:
            point_info = exam_cate_management.auto_create_exam_point(self.cfg, self.driver, self.base_url, self.org_name, point_num=1)
        
            #验证
            for point in point_info:
                xpath = "//div[text()=\'"+point+"\']"
                self.driver.implicitly_wait(2)
                rs = self.is_element_present(By.XPATH, xpath)
                if rs == False:
                    self.verificationErrors.append("fail to create point!")
                    
        except Exception,e:
            print e
            self.verificationErrors.append("fail to create point!")
        finally:
            self.driver.save_screenshot("D:/test_rs_pic/add_point.png")
            
            
            
            
    def modify_exam_point(self):#编辑考点
        
        self.total += 1
        try:
            point_name = exam_cate_management.modify_exam_point(self.cfg,self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to modify point!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/modify_point.png")
            
        #验证
        #xpath = "//div[text()=\'"+point_name+"\']"
        self.driver.implicitly_wait(2)
        #rs = self.is_element_present(By.XPATH, xpath)
        #if rs == False:
            #self.verificationErrors.append("fail to modify subject!")
            
    def delete_exam_point(self):#删除考点
        self.total += 1
        self.total += 1
        try:
            exam_cate_management.delete_exam_point(self.cfg, self.driver, self.base_url, self.org_name)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to delete point!")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/delete_point.png")




    def import_questions(self):
        self.total += 1
        self.template = '//data.ablesky.com/workspace/Testing/Testing Files/Automation_test/createquestions.xls'
        try:
            exam_questions.importquestions(self, self.cfg,self.driver, self.base_url,self.template)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to import questions..")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/create_paper.png")
        
        
    def createpaper(self):
        self.total += 1
        try:
            exam_paper.auto_createpaper(self.cfg, self.driver, self.base_url, 1 ,1, 1,1) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to create paper")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/create_paper.png")
            
    def user_statistical_information(self):
        self.total += 1
        try:
            exam_paper.exam_result(self.cfg, self.driver, self.base_url, exam_name=u"未作答（主观题，免费）", etype=1)
            #exam_paper.exam_result(self.cfg, self.driver, self.base_url, exam_name=u"未作答（主观题，免费）", etype=2)
            #exam_paper.exam_result(self.cfg, self.driver, self.base_url, exam_name=u"未作答（主观题，免费）", etype=3)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to export exam result")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_result.png")
            
    def exam_student_management(self):
        self.total += 1
        try:
            exam_paper.send_close_paper(self.cfg, self.driver, self.base_url, atype=1)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to open paper")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/open_paper.png")
            self.total += 1
        try:
            exam_paper.send_close_paper(self.cfg, self.driver, self.base_url, atype=2)
        except Exception,e:
            print e
            self.verificationErrors.append("fail to close paper")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/close_paper.png")       
    
    def exam_question_danxuan(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_danxuan(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")
               
    def exam_question_duoxuan(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_duoxuan(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")   
 
    def exam_question_shifei(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_shifei(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")   
 
    def exam_question_tiankong(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_tiankong(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")   

    def exam_question_wenda(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_wenda(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")   
    
    def exam_question_wanxing(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_wanxing(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")   

    def exam_question_zonghe(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.exam_question_zonghe(self.cfg, self.driver, self.base_url, question_ansa) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")
            
    def exam_questions(self):
        self.total += 1
        question_ansa='exam' + str(random.randint(1000,9999))
        try:
            exam_questions.auto_exam_questions(self.cfg, self.driver, self.base_url, question_ansa, 1) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to exam questions")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/exam_questions.png")            
            
    def manage_course_num(self):
        self.total += 1
        try:
            student_management.manage_course_num(self.cfg, self.driver, self.base_url) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to manage course num")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/manage_course_num.png")     
    #学员参加考试
    def exam_user(self):
        self.total += 1
        # operation =0 自动提交  operation =1 继续答题
        operation = 1
        question_answer ='123'
        # blank_pager=1是交白卷 ；blank_pager=0 是做了一个题
        blank_pager = 0
        try:
            exam_user_management.exam_user(self.cfg, self.driver, self.base_url, operation, blank_pager, question_answer)
        except Exception,e:
            print e
            self.verificationErrors.append('fail to exam!')
        finally: 
            self.driver.save_screenshot("D:/test_rs_pic/exam_user.png")
            
    def wailian_video(self):
        self.total += 1
        try:
            user_management.wailian_video(self.cfg, self.driver, self.base_url, self.test_enviroment) 
        except Exception,e:
            print e
            self.verificationErrors.append("fail to use wailian")
        finally:
            self.driver.save_screenshot("C:/test_rs_pic/user_management_wailian.png")

    
    def test_regress(self):
        
        #网站主站回归流程
        #self.register()
        self.login_from_index()
        #self.release_normal()
        #self.release_three_video()
        #self.agency_course()
        #self.package_course() 
        #self.add_cate()
        #self.presale_course()  
        #self.add_course_to_cate()   
        #self.prepaid_cardgroup()
        #self.course_cardgroup()
        #self.cate_cardgroup()
        #self.delete_cate()
        #self.buy_listen_card()
        #self.listen_cardgroup()
        #self.add_exam_card()
        self.import_one_student()
        self.import_multi_student()
        self.create_multi_student()
        self.add_admin()  
        self.modify_admin()
        self.delete_admin()
        self.buy_open_num()
        self.release_href_course()
        self.open_course_for_one()
        self.open_course_for_multi()
        self.change_homelogo()
        self.release_announcement()
        self.modify_pagefoot()  
        self.change_headpic()

        self.verify_all_course_convert()

        login.logout(self.driver, self.base_url)
        self.login_user()
        self.use_prepaidcard()
        self.use_coursecard()
        self.use_catecard()
        self.use_listencard()
        self.use_exam_card()
        self.buy_course_use_RMB()
        self.buy_course_use_card() 
          

        
        #self.wailian_video()

        #考试系统部分
        #self.login_from_index()
        #self.exam_question_danxuan()
        #self.exam_question_duoxuan()
        #self.exam_question_shifei()
        #self.exam_question_tiankong()
        #self.exam_question_wenda()
        #self.exam_question_wanxing()
        #self.exam_question_zonghe()
        #self.exam_questions()
        #self.import_questions()
        #self.add_exam_subject()
        #self.modify_exam_subject()
        #self.delete_exam_subject()
        #self.create_exam_cate()
        #self.modify_exam_cate()
        #self.delete_exam_cate() 
        #self.add_exam_point()
        #self.modify_exam_point()
        #self.delete_exam_point()    
        #self.createpaper()
        #self.exam_student_management()
        #self.user_statistical_information()
        #login.logout(self.driver, self.base_url)

        #self.login_user()
        #self.exam_user()
        #self.use_exam_card()
                   

    def tearDown(self):
        self.driver.quit()
        fail_num = len(self.verificationErrors)
        print "total case:%s,%s failures.detail:%s"%(self.total,fail_num,self.verificationErrors)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
