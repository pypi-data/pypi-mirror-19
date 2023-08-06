# coding=utf-8

'''
 :Description:    app驱动库
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
import os
import re
import time
import subprocess
import threading
import inspect
import ctypes
from BElement import BElement
import xml.etree.cElementTree as ET

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class BAndroidDriver(object):
    DeviceId=None
    DeviceName=None
    def __init__(self):
        pass

    def setDeviceId(self,ID):
        if(ID==""):
            ID=None
        self.DeviceId=ID

    def setDeviceName(self,Name):
        self.DeviceName=Name


    def getDeviceName(self):
        return self.DeviceName


    def script(self,script):
        if(self.DeviceId!=None):
           script='adb -s '+self.DeviceId+' '+script.split('adb')[1]
        return os.popen(script).read()

    def getActivitXml(self,FileName):
        self.script('adb shell uiautomator dump /data/local/tmp/' + FileName + '.xml')
        self.script('adb pull /data/local/tmp/' + FileName + '.xml '+PATH(FileName+'.xml'))
        self.script('adb shell rm -r /data/local/tmp/' + FileName + '.xml')

    def click(self,x, y):
        self.script('adb shell input tap ' + str(x) + ' ' + str(y))

    def clickBack(self):
        self.tapKey('KEYCODE_BACK')

    def clickEnter(self):
        self.tapKey('KEYCODE_ENTER')

    def swipe(self,x,y,x1,y1):
        self.script('adb shell input swipe '+ str(x) + ' ' + str(y)+' '+str(x1) + ' ' + str(y1))

    def input(self,text):
        self.script('adb shell input text ' + text)

    def tapKey(self,keycode):
        self.script('adb shell input keyevent ' + keycode)

    def intallApp(self,apkfile):
        self.script('adb install -r '+apkfile)

    def stopApp(self,packge):
        self.script('adb shell am force-stop ' + packge)

    def stsrtApp(self,packge,appActivity):
        self.script('adb shell am start '+ packge+'/'+appActivity)

    def appClearData(self,packge):
        self.script('adb shell pm clear '+packge)

    def clearLog(self):
        self.script('adb logcat -c')

    def getDevices():
        devices=self.script("adb shell devices -l")


    def getPid(self,packgeName):
        Rtu=self.script("adb shell \"ps |grep "+packgeName+" |grep -v :\"")
        if(Rtu==""):
            print(packgeName+" Not have start!")
            return None
        else:
            arr=Rtu.split(' ')
            arr = filter(lambda x:x !='',arr)
            return arr[1]

    def appLog(self,packgeName,Path):
        Pid=self.getPid(packgeName)
        self.getLog("adb shell \"logcat |grep "+str(Pid)+"\"",Path)
    
    def getLog(self,script,Path):
        GG = scriptThread(self,script+" >"+Path)
        GG.start()
        # ctypes.pythonapi.PyThreadState_SetAsyncExc(GG.ident, ctypes.py_object(SystemExit))
        # self.stop_thread(GG)
        return GG
        
    def getElements(self, TypeName, TypeValue):
        """
        同属性多个元素，返回坐标元组列表，[(x1, y1), (x2, y2)]
        """
        BElementList = []
        self.getActivitXml("MarketTest")
        tree = ET.ElementTree(file=PATH("MarketTest.xml"))
        treeIter = tree.iter(tag="node")
        for Element in treeIter:
            if Element.TypeName[TypeName] == TypeValue:
                bounds = Element.TypeName["bounds"]
                coord = self.pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                #将匹配的元素区域的中心点添加进pointList中
                BE=BElement(Xpoint,Ypoint,self)
                BElementList.append(BE)
        return BElementList

    def getElement(self,TypeName,Value):
        BE=BElement()
        if TypeName is "xpath":
            BE = self.getXpathElement(Value)
        else:
            BE = self.getTypeElement(TypeName,Value)
        return BE
    
    def getTypeElement(self,TypeName,TypeValue):
        self.getActivitXml("MarketTest")
        tree = ET.ElementTree(file=PATH("MarketTest.xml"))
        Elements = tree.iter(tag="node")
        Xpoint = 0;
        Ypoint = 0;
        for Element in Elements:
            if Element.attrib[TypeName] == TypeValue:
                bounds = Element.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                Xpoint = (int(bound[0]) + int(bound[2])) / 2
                Ypoint = (int(bound[1]) + int(bound[3])) / 2
        BE=BElement(Xpoint,Ypoint,self)
        return BE


    def getXpathElement(self,xpathValue):
        self.getActivitXml("MarketTest")
        tree = ET.ElementTree(file=PATH("MarketTest.xml"))
        root = tree.getroot()
        for index in xpathValue:
            root = root[index]
        bounds = root.attrib["bounds"]
        pattern = re.compile(r"\d+")
        bound = pattern.findall(bounds)
        Xpoint = (int(bound[0]) + int(bound[2])) / 2
        Ypoint = (int(bound[1]) + int(bound[3])) / 2
        BE=BElement(Xpoint,Ypoint,self)
        return BE

    def _async_raise(self,tid,exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)


class scriptThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self,device,script):
        threading.Thread.__init__(self)
        self.device = device
        self.script = script
    def run(self):
        try:
            print(self.device.DeviceId+"　LogCat...")
            self.device.script(self.script)
        except Exception, e:
            print("Not have connected Device!")