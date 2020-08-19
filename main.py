import pandas as pd
import numpy as np

######根据人数的出生月份、性别比例和所属社区分班。 性别和出生月份通过身份证号获得
######30人一个班



def Birth(id):
    month=int(id[10:12])#生日的位数
    return month
def Sex(id):
    sex=int(id[-2])
    if sex%2==0:
        s = "女"
    else:
        s = "男"
    return s
def GenerateClasses(df):
    relation = [59, 11, 120, 112, 57, 151, 1]###关系户###序号减2
    indexs=np.arange(len(df))
    indexs = [x for x in indexs if x not in relation]
    Class1=np.random.choice(indexs,29-len(relation),replace=False)
    Class1=list(Class1)
    Class1.extend(relation)
    Class1=np.asarray(Class1)
    indexs = [x for x in indexs if x not in Class1]
    Class2=np.random.choice(indexs,30,replace=False)
    indexs = [x for x in indexs if x not in Class2]
    Class3=np.random.choice(indexs,30,replace=False)
    indexs = [x for x in indexs if x not in Class3]
    Class4=np.random.choice(indexs,30,replace=False)
    indexs = [x for x in indexs if x not in Class4]
    Class5=np.random.choice(indexs,30,replace=False)
    indexs = [x for x in indexs if x not in Class5]
    Class6=np.asarray(indexs)
    return Class1,Class2,Class3,Class4,Class5,Class6

def JudgeCommunity(Class1,Class2,Class3,Class4,Class5,Class6):
    for community in ['西安社区','康城社区','联盟社区','水景社区']:
        for Class in [Class1,Class2,Class3,Class4,Class5,Class6]:
            count = 0
            for item in Class:
                if data.values[item][4]==community:###'户籍社区'
                    count=count+1
            if count<4:####每个社区至少4个人
                return False
    return True
def JudgeSex(Class1,Class2,Class3,Class4,Class5,Class6):
    for sex in ['男','女']:
        for Class in [Class1,Class2,Class3,Class4,Class5,Class6]:
            man = 0
            woman = 0
            for item in Class:
                s = Sex(data.values[item][1])
                if s == '男':
                    man += 1
                else:
                    woman += 1
            ratio=man/woman
            # if ratio<=0.76 and ratio>=1.4:##13+17
            if ratio <= 0.87 and ratio >= 1.15:  ##14+16
                return False
    return True
def JudgeBirth(Class1,Class2,Class3,Class4,Class5,Class6):
    for i in range(12):
        count=0
        for Class in [Class1,Class2,Class3,Class4,Class5,Class6]:
            for item in Class:
                if Birth(data.values[item][1])==i+1:
                    count=count+1
            if count<1:###每个月至少一个人
                return False
    return True




data = pd.read_excel('info.xlsx')####读取源文件
print(data.head())
data['身份证']=data['身份证'].astype(str)
###########数据读取完毕########
man=0
woman=0
for item in range(len(data.values)):
    s=Sex(data.values[item][1])
    if s=='男':
        man+=1
    else:
        woman+=1
sex_ratio=man/woman####0.967
print('男女比: {}'.format(sex_ratio))

flag=1
loop=0
while (flag):
    Class1,Class2,Class3,Class4,Class5,Class6=GenerateClasses(data)
    birth_value=JudgeBirth(Class1,Class2,Class3,Class4,Class5,Class6)
    community_value=JudgeCommunity(Class1,Class2,Class3,Class4,Class5,Class6)
    Sex_value=JudgeSex(Class1,Class2,Class3,Class4,Class5,Class6)
    if Sex_value and community_value and birth_value:
        break


writer=pd.ExcelWriter('results.xlsx')
data.loc[Class1].to_excel(writer,sheet_name='Class1',index=0)
data.loc[Class2].to_excel(writer,sheet_name='Class2',index=0)

data.loc[Class3].to_excel(writer,sheet_name='Class3',index=0)
data.loc[Class4].to_excel(writer,sheet_name='Class4',index=0)
data.loc[Class5].to_excel(writer,sheet_name='Class5',index=0)
data.loc[Class6].to_excel(writer,sheet_name='Class6',index=0)

writer.save()
writer.close()
