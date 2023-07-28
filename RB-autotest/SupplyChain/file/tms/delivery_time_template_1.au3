ControlFocus("打开","text","Edit1")
WinWait("[CLASS:#32770]","",10)
;ControlSetText("打开","","Edit1","D:\upload_file.txt")  这里的“text” 不必写，写就不能正确执行了
;ControlSetText("打开","","Edit1","C:\Users\chenpeng\Desktop\test_file\delivery_time_template.xls")
ControlSetText("打开","","Edit1",$CmdLine[1])
Sleep(2000)
ControlClick("打开","","Button1")