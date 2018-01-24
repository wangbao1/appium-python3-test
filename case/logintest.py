# encoding: utf-8
'''
@author: lileilei
@file: logintest.py
@time: 2017/4/26 21:09
'''
from appium import webdriver
import yaml, unittest, time
from public.logout_pub import logout
from log.log_case import Logger
from public.login_pub import Login


class Logintest(unittest.TestCase):
    def setUp(self):
        title = '启动测试'
        # self.dis_app = {}
        # self.dis_app['platformName'] = 'Android'
        # self.dis_app['platformVersion'] = '7.0'
        # self.dis_app['deviceName'] = 'Android Emulator'
        # self.dis_app['appPackage'] = 'com.newsdog'
        # self.dis_app['appActivity'] = 'com.newsdog.mvp.ui.splash.SplashActivity'
        # self.dis_app['androidDeviceReadyTimeout'] = 30
        # # self.dis_app['unicodeKeyboard']=True
        # # self.dis_app['resetKeyboard']=True
        # self.driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', self.dis_app)

        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '7.0'
        # self.desired_caps['platformVersion'] = '5.0'
        self.desired_caps['deviceName'] = 'Android Emulator'
        self.desired_caps['appPackage'] = 'com.newsdog'
        self.desired_caps['appActivity'] = 'com.newsdog.mvp.ui.splash.SplashActivity'
        # self.desired_caps['app'] = PATH('api/NewsDog_v2.4.4_newsdog_GooglePlay.apk_2.4.4.apk')

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

        time.sleep(10)
        self.logcan = Logger(title)
        # self.data = self.data['login']
        # self.logut = logout(self.deriver)
        self.logs = Login(self.driver)

    def test_login_1(self):
        """首次启动"""
        try:
            self.driver.find_element_by_id("android:id/button1").click()
            time.sleep(2)
            self.driver.find_element_by_id("android:id/button1").click()
            time.sleep(2)
            self.driver.find_element_by_id("com.newsdog:id/en_tv").click()
            time.sleep(2)
        except Exception as e:
            self.logcan.error_log(u'失败原因：%s' % e)
            print('login1 fail,reson:%s' % e)

    def test_login_2(self):
        try:
            self.driver.find_elements_by_id("com.newsdog:id/news_item_title_tv")[0].click()
            self.driver.press_keycode(4)
            for i in range(18):
                self.driver.swipe(900, 900, 300, 900, 500)
                self.driver.find_elements_by_id("com.newsdog:id/news_item_title_tv")[0].click()
                self.driver.press_keycode(4)
        except Ellipsis as e:
            self.driver.find_element_by_id("com.newsdog:id/next_time_tv").click()
            print("出现分享弹层")
            self.driver.close_app()
            self.driver.launch_app()


    def test_login_3(self):
        try:
            self.driver.find_elements_by_id("com.newsdog:id/news_item_title_tv")[0].click()
            self.driver.press_keycode(4)
            for i in range(18):
                self.driver.swipe(900, 900, 300, 900, 500)
                self.driver.find_elements_by_id("com.newsdog:id/news_item_title_tv")[0].click()
                self.driver.press_keycode(4)
        except Ellipsis as e:
            self.driver.find_element_by_id("com.newsdog:id/next_time_tv").click()
            print("出现分享弹层")


    def tearDown(self):
        self.driver.quit()
if __name__=="__main__":
    test = Logintest()
    test.setUp()
    test.test_login_1()
    test.test_login_2()
    test.test_login_3()