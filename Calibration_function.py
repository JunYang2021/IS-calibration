#coding=utf-8
import pandas as pd
import numpy as np
def Calibrate(sheet):
    sheet[sheet=='N/F']=np.nan
    sheet=sheet.set_index('Compound')
    #将QC的名字存储在一个列表中（通过产生QCorNot的Series，根据布尔索引选取index得到QC的名称）
    QC_series=sheet.loc['QC(1)orNot(0)']
    QC_list=QC_series[QC_series==1].index
    #制作数据质量页，找出内标.数据质量通过返回IS得到
    IS=sheet[sheet['IS(1)orNot(0)']==1][QC_list]
    for i in IS.index:
        IS.loc[i,"rsd in QCs"]=IS.loc[i,QC_list].std()/IS.loc[i,QC_list].mean()
    result1=IS.drop(QC_list,axis=1)
    #处理QC中的数据
    result2=sheet[sheet['IS(1)orNot(0)']==0][QC_list]
    for i in result2.index:
        a=[0,0]
        for j in IS.index:
            division_list=result2.loc[i,QC_list]/IS.loc[j,QC_list]
            x=division_list.std()/division_list.mean()
            if a[0]==0 or a[0]>x:
                a[0]=x
                a[1]=j
            result2.loc[i,"by %s"%j]=x
        result2.loc[i,"minium"]=a[0]
        result2.loc[i,"CalibrationIS"]=a[1]
    result2=result2.drop(QC_list,axis=1)
    #对原始数据进行处理（先得到样本名的集合，因为表格ISorNot会对结果产生影响）
    sample_list = QC_series[pd.notnull(QC_series)].index
    IS_data=sheet[sheet['IS(1)orNot(0)']==1][sample_list]
    Compound_data=sheet[sheet['IS(1)orNot(0)']==0][sample_list]
    result3=Compound_data
    for i in Compound_data.index:
        result3.loc[i]=Compound_data.loc[i]/IS_data.loc[result2.loc[i,"CalibrationIS"]]
    #返回3个DataFrame
    return result1,result2,result3

if __name__=='__main__':
    sheet1=pd.read_excel('20210605_dy_pos(1).xlsx')
    Calibrate(sheet1)