ControlFocus("��","text","Edit1")
WinWait("[CLASS:#32770]","",10)
;ControlSetText("��","","Edit1","D:\upload_file.txt")  ����ġ�text�� ����д��д�Ͳ�����ȷִ����
;ControlSetText("��","","Edit1","C:\Users\chenpeng\Desktop\test_file\delivery_time_template.xls")
ControlSetText("��","","Edit1",$CmdLine[1])
Sleep(2000)
ControlClick("��","","Button1")