import pandas as pd
import copy

path_list = []
for i in range(10,21,2):
    path_list.append(r"D:\cfpsdata\cfps"+"20%s"%i+"家庭经济.dta")
    path_list.append(r"D:\cfpsdata\cfps"+"20%s"%i+"家庭关系.dta")
    if i<17:
        path_list.append(r"D:\cfpsdata\cfps"+"20%s"%i+"成人库.dta")
    else:
        path_list.append(r"D:\cfpsdata\cfps"+"20%s"%i+"个人库.dta")
for j in path_list:
    a = pd.read_stata(j,convert_categoricals=False)
        #由于CFPS的value labels不唯一，因此convert_categoricals=False
    a_1 = copy.copy(a)
        #深拷贝一份，方便后面做填充
    with pd.io.stata.StataReader(j) as reader:
        lb = reader.variable_labels()
            #读取变量标签
        vl = reader.value_labels()
            #读取值标签
    for k in vl.keys():
        a[k] = a[k].map(vl[k],na_action='ignore')
            #将值标签字典映射到a，但是部分正常数据会被替换成NaN
    for k in a.columns:
        a[k].fillna(value=a_1[k], inplace=True)
            #用深拷贝的填充a的NaN        
    b = pd.DataFrame(dict(lb = lb)).T
        #变量标签导出
    c = pd.concat([a,b])
        #变量标签合并
    last_row = pd.DataFrame(c.iloc[-1]).T
    d = pd.concat([last_row,a])
    d.to_csv(j[12:-4]+".csv",index=False,encoding='utf-8-sig')
        #导出为csv



