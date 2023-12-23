#coding=utf-8
#用户输入文件的绝对路径，生成sheet_names的列表
import pandas as pd
from datetime import date
import Calibration_function
file_name=input("请输入文件的绝对路径\n")
file=pd.ExcelFile(file_name)
writer=pd.ExcelWriter("%s校正结果.xlsx"%date.today().strftime('%Y%m%d'),mode='w')
for i in range(len(file.sheet_names)):
    sheeti=pd.read_excel(file_name,sheet_name=i)
    #调用Calibration_function对原始数据进行处理，函数返回3个DataFrame，接收后生成excel
    result1,result2,result3=Calibration_function.Calibrate(sheeti)
    #将结果转化为excel
    result1.to_excel(writer, sheet_name=file.sheet_names[i] + '数据质量', na_rep='N/F')
    result2.to_excel(writer, sheet_name=file.sheet_names[i] + '选择校正内标', na_rep='N/F')
    result3.to_excel(writer, sheet_name=file.sheet_names[i] + '校正结果', na_rep='N/F')
writer.save()
writer.close()