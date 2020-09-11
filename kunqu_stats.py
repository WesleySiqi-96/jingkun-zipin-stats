import re
import unicodecsv
import numpy as np
from zhconv import convert as cv
from urllib.request import urlopen
from xlwt import Workbook
from pan_ding import *

def qupu():
    zidict = {}
    file = open('./data/昆曲曲谱代码.txt', 'r')
    dirclist=file.readlines()
    for dirc in dirclist:
        url1='https://gongchepu.net'+dirc
        html = urlopen(
            url1
        ).read().decode('utf-8')
        pat2=re.compile(r"#[\u4e00-\u9fa5]+[\s\S]+</div><div class=\"paper-container paper-layout-hscroll\">")
        i=str(re.findall(pat2,html))[1:-2]

        pu = re.sub("[\\\\a-zA-Z' ]+",'',i )
        pu=re.sub('[{](.*?)[}]','',pu)
        pu = re.sub('[(](.*?)[)]', '', pu)
        pu = re.sub('[【](.*?)[】]', '', pu)
        pu = re.sub('[<](.*?)[>]', '', pu)
        pu = re.sub('[（](.*?)[）]', '', pu)
        pu = re.sub('=|。|，|、|……|；|#|&|"|“|”|;|,|？|！|!|\?|﻿：|﻿:', '', pu)
        dontconv=['干','余','发','云','后','面','脏','吓','从','﻿㕶','只','才','斗','历','吁','郁','征','胡','钟','面','咸'
                  ,'须','岳','周','游']
        for zi in pu:
            if cv(zi,'zh-hans') in dontconv:
                pass
            else:
                zi=cv(zi,'zh-hans')

            if zi in zidict:
                zidict[zi]+=1
            else:
                zidict[zi]=1
    with open('./统计结果/昆曲字频.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile,encoding='utf-8-sig')
        for key, value in zidict.items():
            writer.writerow([key,value])

def jiantuan():
    csvFile = open("./统计结果/昆曲字频.csv", "rb")
    reader = unicodecsv.reader(csvFile,encoding='utf-8-sig')
    zidict = []
    for item in reader:

        zidict.append(item)

    a=sorted(zidict, key=lambda x: int(x[1]), reverse=True)

    t500=np.array(a[0:500])
    t1000=np.array(a[0:-1])
    wb = Workbook()
    st1=wb.add_sheet('入声及尖团')
    st1.write(0, 0, '昆曲入声及尖团字统计，计频率前800')
    st1.write(1,0,'顺序')
    st1.write(1,1,'字')
    st1.write(1, 2, '尖团')
    st1.write(1, 3, '声调')
    st1.write(1, 4, '频率(%)')


    st2 = wb.add_sheet('尖团')
    st2.write(0, 0, '昆曲尖团字统计，计频率前500')
    st2.write(1, 0, '顺序')
    st2.write(1, 1, '字')
    st2.write(1, 2, '尖团')
    st2.write(1, 3, '频率(%)')



    st3 = wb.add_sheet('入声')
    st3.write(0, 0, '昆曲入声字统计，计频率前500')
    st3.write(1, 0, '顺序')
    st3.write(1, 1, '字')
    st3.write(1, 2, '频率(%)')


    n1 = 1
    n2=1
    n3=1
    #style = xlwt.easyxf(' color red;')
    for count in range(len(t1000[:,0])):
        freq=int(t1000[count,1])/np.sum(t1000[:,1].astype(float))*100
        i=t1000[count,0]

        if isjian(i)=='非'and isru(i)=='非入' :
            continue
        else:
            if n1<801:
                st1.write(n1 + 1, 0, n1)
                st1.write(n1+1, 1, i)
                st1.write(n1+1, 2, isjian(i))
                st1.write(n1+1, 3, isru(i))

                if round(freq,2)==0:
                    st1.write(n1 + 1, 4,'<0.01')
                else:
                    st1.write(n1+1, 4, round(freq,2))
                n1+=1

        if isjian(i) in ['尖','团'] and n2<501:
            st2.write(n2 + 1, 0, n2)
            st2.write(n2+1, 1, i)
            st2.write(n2 + 1, 2, isjian(i))
            if round(freq,2)==0:
                st2.write(n2 + 1, 3,'<0.01')
            else:
                st2.write(n2+1, 3, round(freq,2))
            n2+=1

        if isru(i)=='入声'and n3<501:
            st3.write(n3 + 1, 0, n3)
            st3.write(n3+1, 1, i)

            if round(freq,2)==0:
                st3.write(n3 + 1, 2,'<0.01')
            else:
                st3.write(n3+1, 2, round(freq,2))
            n3+=1



    wb.save('./统计结果/昆曲入声及尖团统计.xls')


#执行顺序
qupu()#字频统计
jiantuan()#尖团，入声分析
