lis = ["Cote D'ivoire (ivory Coast)", 'Cocos (keeling) Islands','Virgin Islands, Us']
# 去除lis_new列表中 ， （）  '   然后用 - 连接所有单词
# 转换成 lis = ["Cote-Divoire-ivory-Coast", 'Cocos-keeling-Islands','Virgin-Islands-Us']

for i in lis:
    L = i.replace("'","")
    L1=L.replace("(","")
    L2 = L1.replace(")", "")
    L3 = L2.replace(",", "")
    L4 = L3.replace(" ", "-")
    print(L4)
print(lis)

print('----------转换后---------')
print('Cote-Divoire-ivory-Coast')
print('Cocos-keeling-Islands')
print('Virgin-Islands-Us')
