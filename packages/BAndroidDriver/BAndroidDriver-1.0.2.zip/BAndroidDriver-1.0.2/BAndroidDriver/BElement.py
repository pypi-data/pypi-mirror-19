# coding=utf-8
import time
'''
 :Description:    控件类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
class BElement(object):
	def __init__(self,x,y,device):
		self.Xpoint=x
		self.Ypoint=y
		self.device=device

	# def setXY(self):
	# 	self.Xpoint=x
	# 	self.Ypoint=y
	# 	self.device=device
	def click(self):
		self.device.Click(self.Xpoint,self.Ypoint)

	def Input(self,Str):
		self.click()
		time.sleep(1)
		self.device.Input(Str)