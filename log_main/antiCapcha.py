#coding=gbk
#第一行注释不能省，指定编码声明以支持中文
#本代码文件在32位的python 3.3.2版测试通过
import urllib
import time
import string
import ctypes
from ctypes import * 

dll = ctypes.windll.LoadLibrary('AntiVC.dll')
#如果dll不在当前目录，那么需要指定全路径

#dll.UseUnicodeString(True)#这个函数用来向DLL说明传入传出的文本均使用unicode格式

CdsIndex = dll.LoadCdsFromFile('Python.cds','424302950')
#如果识别库不在当前目录，那么需要指定全路径

if(CdsIndex == -1):
	print('LoadCds Fail!')#注意缩进格式
else:
	print('LoadCds Success:',CdsIndex)#LoadCdsFromFile调用一次即可，无需重复调用
	
def GetCode(imgaeName):
	# Decode the string in the image and return the code, Alan
	Str = create_string_buffer(4)#创建文本缓冲区
	if(dll.GetVcodeFromFile(CdsIndex,imgaeName,Str)):
		code = Str.raw.decode("utf-8")
		#如果验证码图像不在当前目录，那么需要指定全路径
		print('GetVcode Success:',code)
		#返回的文本需解码后才能正常显示
	else:
		code = None
		print('GetVcode Fail!')
	return code 
