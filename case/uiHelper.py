# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:        UiHelper
# Purpose:
#
# Author:      alexsczhong
#
# Created:     11/09/2014
# Copyright:   (c) Tencent 2014
# Licence:     All rights reserved
# -------------------------------------------------------------------------------

import sys
import os
from appium import webdriver
from time import sleep
import time
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

"""
Connection types are specified here:
    https://code.google.com/p/selenium/source/browse/spec-draft.md?repo=mobile#120
    Value (Alias)      | Data | Wifi | Airplane Mode
    -------------------------------------------------
    0 (None)           | 0    | 0    | 0
    1 (Airplane Mode)  | 0    | 0    | 1
    2 (Wifi only)      | 0    | 1    | 0
    4 (Data only)      | 1    | 0    | 0
    6 (All network on) | 1    | 1    | 0
"""


class ConnectionType(Enum):
    NO_CONNECTION = 0
    AIRPLANE_MODE = 1
    WIFI_ONLY = 2
    DATA_ONLY = 4
    ALL_NETWORK_ON = 6


class UiHelper:
    remoteHost = "http://127.0.0.1:4723/wd/hub"

    def __init__(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '7.0'
        # self.desired_caps['platformVersion'] = '5.0'
        self.desired_caps['deviceName'] = 'Android Emulator'
        self.desired_caps['appPackage'] = 'com.newsdog'
        self.desired_caps['appActivity'] = 'com.newsdog.mvp.ui.splash.SplashActivity'
        # self.desired_caps['app'] = PATH('api/NewsDog_v2.4.4_newsdog_GooglePlay.apk_2.4.4.apk')

        self._driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

    def quitDriver(self):
        if self._driver:
            self._driver.quit()

    """
        判断有没有广告和评价的弹层影响正常数据
    """
    def advert(self):
        try:
            self.findElement("Like NewsDog?")
            self.findElement("Next Time").click()
            print("you评价弹层")
        except:
            pass
        try:
            self.findElement("5 stars for me?")
            self.findElement("Next Time").click()
            print("you评价弹层")
        except:
            pass
        while self.checkElementIsShown("com.newsdog:id/pw"):
            self.findElement("com.newsdog:id/pw")
            self.swipe(500, 900, 500, 300, 1000)
            self.swipe(500, 900, 500, 300, 1000)
            print("you广告")

    """
    给定控件的xpatch, id 或者name来查找控件

    :Args:
         - controlInfo: 控件的信息，可以是xpath,id或者其他属性

    :Return:
        如果找到控件，返回第一个

    :Usage:
        self.findElement(controlInfo)
    """
    def findElement(self, controlInfo):
        if controlInfo.startswith("//"):
            element = self._driver.find_element_by_xpath(controlInfo)
        elif ":id/" in controlInfo or ":string/" in controlInfo:
            element = self._driver.find_element_by_id(controlInfo)
        else:
            # 剩下的字符串没有特点，无法区分，因此先尝试通过名称查找
            try:
                element = self._driver.find_element_by_name(controlInfo)
            except:
                # 如果通过名称不能找到则通过class name查找
                element = self._driver.find_element_by_class_name(controlInfo)
        return element

    """
    给定控件的xpatch, id 或者name来查找控件

    :Args:
         - controlInfo: 控件的信息，可以是xpath,id或者其他属性

    :Return:
        返回所有满足条件的控件，返回的类型是一个列表

    :Usage:
        self.findElements(controlInfo)
    """

    def findElements(self, controlInfo):
        if controlInfo.startswith("//"):
            elements = self._driver.find_elements_by_xpath(controlInfo)
        elif ":id/" in controlInfo:
            elements = self._driver.find_elements_by_id(controlInfo)
        else:
            elements = self._driver.find_elements_by_name(controlInfo)
            if len(elements) == 0:
                elements = self._driver.find_elements_by_class_name(controlInfo)
        return elements

    """
    在一个已知的控件中通过给定控件的xpatch, id 或者name来查找子控件

    :Args:
        - parentElement: 父控件，是一个已知的WebElement
        - childElementInfo: 子控件的信息，可以是xpath,id或者其他属性

    :Return:
        如果找到控件，返回第一个

    :Usage:
        self.findElement(controlInfo)
    """

    def findElementInParentElement(self, parentElement, childElementInfo):
        if childElementInfo.startswith("//"):
            element = parentElement.find_element_by_xpath(childElementInfo)
        elif ":id/" in childElementInfo:
            element = parentElement.find_element_by_id(childElementInfo)
        else:
            # 剩下的字符串没有特点，无法区分，因此先尝试通过名称查找
            try:
                element = parentElement.find_element_by_name(childElementInfo)
            except:
                # 如果通过名称不能找到则通过class name查找
                element = parentElement.find_element_by_class_name(childElementInfo)

        return element

    """
    在一个已知的控件中通过给定控件的xpatch, id 或者name来查找子控件

    :Args:
        - parentElement: 父控件，是一个已知的WebElement
        - childElementInfo: 子控件的信息，可以是xpath,id或者其他属性

    :Return:
        如果找到控件，返回所有符合条件的控件

    :Usage:
        self.findElementsInParentElement(parentElement, controlInfo)
    """

    def findElementsInParentElement(self, parentElement, childElementInfo):
        if childElementInfo.startswith("//"):
            elements = parentElement.find_elements_by_xpath(childElementInfo)
        elif ":id/" in childElementInfo:
            elements = parentElement.find_elements_by_id(childElementInfo)
        else:
            # 剩下的字符串没有特点，无法区分，因此先尝试通过名称查找
            elements = parentElement.find_elements_by_name(childElementInfo)
            if len(elements) == 0:
                # 如果通过名称不能找到则通过class name查找
                elements = parentElement.find_elements_by_class_name(childElementInfo)

        return elements

    """
    通过UIAutomator的uia_string来查找控件

    :Args:
        -uia_string: UiSelector相关的代码，参考http://developer.android.com/
        tools/help/uiautomator/UiSelector.html#fromParent%28com.android.uiautomator.core.UiSelector%29

    :Return:
        -找到的控件

    :usage:
        self.findElementByUIAutomator(new UiSelector().(android.widget.LinearLayout))
    """

    def findElementByUIAutomator(self, uia_string):
        return self._driver.find_element_by_android_uiautomator(uia_string)

    """
    滑动操作

    :Args:
         - x1,y1,x2,y2： 滑动操作的起点和终点的坐标

    :Usage:
        self.swipe(50, 50, 400, 400)
    """

    def flick(self, x1, y1, x2, y2):
        self._driver.flick(x1, y1, x2, y2)

    """
    滑动操作

    :Args:
         - x1,y1,x2,y2： 滑动操作的起点和终点的坐标
         - peroid: 多长时间内完成该操作,单位是毫秒

    :Usage:
        self.swipe(50, 50, 400, 400, 500)
    """

    def swipe(self, x1, y1, x2, y2, peroid):
        self._driver.swipe(x1, y1, x2, y2, peroid)

    def tap(self, x, y):
        self._driver.tap([(x, y)])

    """
    长按点击操作
    :Args:
     - x,y： 长按点的坐标
     - peroid: 多长时间内完成该操作,单位是毫秒

    :Usage:
        self.longPress(50, 50, 500)
    """

    def longPress(self, x, y, peroid):
        self._driver.tap([(x, y)], peroid)

    """
    点击某一个控件，如果改控件不存在则会抛出异常

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性

    :Usage:
        self.clickElement(elementInfo)
    """

    def clickElement(self, elementInfo):
        element = self.findElement(elementInfo)
        element.click()

    """
    获取某个控件显示的文本，如果该控件不能找到则会抛出异常

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性

    :Return:
        返回该控件显示的文本

    :Usage:
        self.getTextOfElement(elementInfo)

    """

    def getTextOfElement(self, elementInfo):
        element = self.findElement(elementInfo)
        return element.text

    """
    清除文本框里面的文本

    :Usage:
        self.clearTextEdit(elementInfo)
    """

    def clearTextEdit(self, elementInfo):
        element = self.findElement(elementInfo)
        element.clear()

    """
    按返回键

    :Usage:
        self.pressBackKey()
    """

    def pressBackKey(self):
        # code码参考Android的官网的keycode
        self._driver.press_keycode(4)

    """
    等待某个控件显示

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性
         - period：等待的秒数

    :Usage:
        self.waitForElement(elementInfo, 3)
    """

    def waitForElement(self, elementInfo, period):
        for i in range(0, period):
            try:
                self.findElement(elementInfo)
                return
            except:
                sleep(1)
                continue

        raise Exception("Cannot find %s in %d seconds" % (elementInfo, period))

    """
    等待某个控件不再显示

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性
         - period：等待的秒数

    :Usage:
        self.waitForElementNotPresent(elementInfo, 3)
    """

    def waitForElementNotPresent(self, elementInfo, period):
        for i in range(0, period):
            sleep(1)
            # 不存在了则返回
            if not self.checkElementIsShown(elementInfo):
                return
            else:
                continue

        raise Exception("Cannot find %s in %d seconds" % (elementInfo, period))

    """
    判断某个控件是否显示

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性
    :Return:
        True: 如果当前画面中期望的控件能被找到

    :Usage:
        self.checkElementIsShown(elementInfo)
    """

    def checkElementIsShown(self, elementInfo):
        try:
            self.findElement(elementInfo)
            return True
        except:
            return False

    """
    判断某个控件是否显示在另外一个控件中

    :Args:
        - parentElement: 父控件，是一个已知的WebElement
        - childElementInfo: 子控件的信息，可以是xpath,id或者其他属性
    :Return:
        True: 如果当前画面中期望的控件能被找到

    :Usage:
        self.checkElementShownInParentElement(elementInfo)
    """

    def checkElementShownInParentElement(self, parentElement, childElementInfo):
        try:
            self.findElementInParentElement(parentElement, childElementInfo)
            return True
        except:
            return False

    """
    判断某个控件是否被选中

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性
    :Return:
        True: 如果当前画面中期望的控件能被选中

    :Usage:
        self.checkElementIsSelected(elementInfo)
    """

    def checkElementIsSelected(self, elementInfo):
        element = self.findElement(elementInfo)
        return element.is_selected()

    """
    判断某个开关控件是否被选中

    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性
    :Return:
        True: 如果当前画面中期望的控件能被选中

    :Usage:
        self.checkElementIsChecked(elementInfo)
    """

    def checkElementIsChecked(self, elementInfo):
        element = self.findElement(elementInfo)
        if element.get_attribute("checked") == "false":
            return False
        else:
            return True

    """
    判断摸个控件是否enabled
    :Args:
         - elementInfo: 控件的信息，可以是xpath,id或者其他属性
    :Return:
        True: 如果当前画面中期望的控件enabled

    :Usage:
        self.checkElementIsEnabled(elementInfo)
    """

    def checkElementIsEnabled(self, elementInfo):
        element = self.findElement(elementInfo)
        return element.get_attribute("enabled")

    """
    获取当前的Activity

    :Return:
        当前Activity的名称
    """

    def getCurrentActivity(self):
        return self._driver.current_activity

    """
    等待某一个Activity显示
    备注：不确定是否适用于ios

    :Args:
        -activityName: 某acitivity的名称
        -period: 等待的时间，秒数
    """

    def waitForActivity(self, activityName, period):
        for i in range(0, period):
            sleep(1)
            try:
                if activityName in self.getCurrentActivity():
                    return
            except:
                continue

        raise Exception("Cannot find the activity %s in %d seconds" % (activityName, period))

    """
    保存当前手机的屏幕截图到电脑上指定位置

    :Args:
         - pathOnPC: 电脑上保存图片的位置

    :Usage:
        self.saveScreenshot("c:\test_POI1.jpg")
    """

    def saveScreenshot(self, pathOnPC):
        self._driver.save_screenshot(pathOnPC)

    def setNetwork(self, netType):
        pass

    """
    启动测试程序
    """

    def launchApp(self):
        self._driver.launch_app()

    """
    关闭测试程序
    """

    def closeApp(self):
        self._driver.close_app()

    """
    获取测试设备的OS

    :Return: Android或者ios
    """

    def getDeviceOs(self):
        return self.desired_caps['platformName']

    """
    只打开wifi连接
    """

    def enableWifiOnly(self):
        if (self._driver.network_connection & 0x2) == 2:
            return
        else:
            self._driver.set_network_connection(ConnectionType.WIFI_ONLY)

    """
    只打开数据连接
    """

    def enableDataOnly(self):
        if int(self._driver.network_connection & 4) == 4:
            return
        else:
            self._driver.set_network_connection(ConnectionType.DATA_ONLY)

    """
    关闭所有网络连接
    """

    def disableAllConnection(self):
        self._driver.set_network_connection(ConnectionType.NO_CONNECTION)

    """
    获取context
    """

    def getContext(self):
        self._driver.contexts

    def switchContext(self, contextName):
        self._driver.switch_to.context(contextName)

    """
    打开所有的网络连接
    """

    def enableAllConnection(self):
        self._driver.set_network_connection(ConnectionType.ALL_NETWORK_ON)

    @property
    def driver(self):
        return self._driver
