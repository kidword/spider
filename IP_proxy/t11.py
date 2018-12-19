

num = input("请输入：",)
str1 = 'a2bc3d1'   # aabcbcbcd
if type(int(num))== int:
    print("输入的全是数字,请重新输入")

for i in range(len(num)):

    str2 = ""
    try:
        num = []
        int(num[i])
        num.append(int(num[i]))
    except:
        #str1.join(num[i])
        pass
    print(num)
        # if type(num[i]) == str:
    #     print('num[i]', num[i])
