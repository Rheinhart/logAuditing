#coding=gbk
#��һ��ע�Ͳ���ʡ��ָ������������֧������
#�������ļ���32λ��python 3.3.2�����ͨ��
import urllib
import time
import string
import ctypes
from ctypes import * 

dll = ctypes.windll.LoadLibrary('AntiVC.dll')
#���dll���ڵ�ǰĿ¼����ô��Ҫָ��ȫ·��

#dll.UseUnicodeString(True)#�������������DLL˵�����봫�����ı���ʹ��unicode��ʽ

CdsIndex = dll.LoadCdsFromFile('Python.cds','424302950')
#���ʶ��ⲻ�ڵ�ǰĿ¼����ô��Ҫָ��ȫ·��

if(CdsIndex == -1):
	print('LoadCds Fail!')#ע��������ʽ
else:
	print('LoadCds Success:',CdsIndex)#LoadCdsFromFile����һ�μ��ɣ������ظ�����
	
def GetCode(imgaeName):
	# Decode the string in the image and return the code, Alan
	Str = create_string_buffer(4)#�����ı�������
	if(dll.GetVcodeFromFile(CdsIndex,imgaeName,Str)):
		code = Str.raw.decode("utf-8")
		#�����֤��ͼ���ڵ�ǰĿ¼����ô��Ҫָ��ȫ·��
		print('GetVcode Success:',code)
		#���ص��ı����������������ʾ
	else:
		code = None
		print('GetVcode Fail!')
	return code 
