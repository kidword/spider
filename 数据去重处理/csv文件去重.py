# 将两个csv文件合并，去除重复数据
import csv
import pandas as pd

#read = pd.read_csv(r'd:\no.csv',encoding = 'gb18030')

def readCSV2List(filePath):
    try:
        file=open(filePath,'r',encoding="gb18030")# 读取以utf-8
        context = file.read() # 读取成str
        list_result=context.split("\n")#  以回车符\n分割成单独的行
        #每一行的各个元素是以【,】分割的，因此可以
        length=len(list_result)
        for i in range(length):
            list_result[i]=list_result[i].split(",")
        return list_result
    except Exception :
        print("文件读取转换失败，请检查文件路径及文件编码是否正确")
    finally:
        file.close();# 操作完成一定要关闭
list1 = readCSV2List(r'D:\暂无机场信息列表.csv')
list2 = readCSV2List(r'D:\暂无机场信息列表.csv')
#print(len(list1))
list3 = list1+list2
for i in list3:
    lis = i[1:-2]
    #print(lis)
print(list3)

