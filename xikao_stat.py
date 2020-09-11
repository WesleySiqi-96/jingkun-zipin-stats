import re
import unicodecsv
import numpy as np
from urllib.request import urlopen
from xlwt import Workbook
import os
from pan_ding import isjian


def statss():
    zidict = {}
    allf=os.listdir('./xikao/')
    for name in allf:
        file = open('./xikao/' + name, 'r')
        f=[]
        f=file.read()
        for cha in f:
            if cha in zidict:
                zidict[cha] += 1
            else:
                zidict[cha] = 1
        file.close()
    with open('./output/戏考字频.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile, encoding='utf-8-sig')
        for key, value in zidict.items():
            writer.writerow([key, value])

def jianzi2():
    csvFile = open("./output/戏考字频.csv", "rb")
    reader = unicodecsv.reader(csvFile, encoding='utf-8-sig')
    zidict = []
    for item in reader:
        zidict.append(item)

    a = sorted(zidict, key=lambda x: int(x[1]), reverse=True)
    t1000 = np.array(a[0:-1])


    wb = Workbook()
    st1 = wb.add_sheet('尖团')
    st1.write(0, 0, '京剧尖团字统计，计频率前500')
    st1.write(1, 0, '顺序')
    st1.write(1, 1, '字')
    st1.write(1, 2, '尖团')
    st1.write(1, 3, '频率(%)')

    n1=1
    for count in range(len(t1000[:,0])):
        freq=int(t1000[count,1])/np.sum(t1000[:,1].astype(float))*100
        i=t1000[count,0]

        if isjian(i) in ['尖','团'] and n1 < 501:
            st1.write(n1 + 1, 0, n1)
            st1.write(n1 + 1, 1, i)
            st1.write(n1 + 1, 2, isjian(i))

            if round(freq, 2) == 0:
                st1.write(n1 + 1, 3, '<0.01')
            else:
                st1.write(n1 + 1, 3, round(freq, 2))
            n1 += 1

    wb.save('京剧尖团统计.xls')


statss()#字频统计
jianzi2()#尖团分析