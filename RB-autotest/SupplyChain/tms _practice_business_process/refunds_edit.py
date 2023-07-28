import openpyxl
import random
wb=openpyxl.load_workbook(r'C:\Users\chenpeng\Desktop\test_file\cod_refunds.xlsx')
print(wb.sheetnames)
# sheet=wb.get_sheet_by_name('返款对账')
sheet=wb['返款对账']
print(sheet.title)
sheet02=wb.active
print(sheet02.title)
print(sheet['A2'].value)  #获取单元格A1值
print(sheet['B2'].value)  #获取单元格A1值
print(sheet['C2'].value)  #获取单元格A1值
# print(sheet['B2'].column)  #获取单元格列值
# print(sheet['C2'].row)  #获取单元格行号
i=random.randint(1,100)
sheet['C2'] =i  # 直接修改A1单元格的值为A1
print(sheet['C2'].value)
wb.save(r'C:\Users\chenpeng\Desktop\test_file\cod_refunds.xlsx')
