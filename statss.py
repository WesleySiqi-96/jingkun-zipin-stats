import re
import unicodecsv
import numpy as np
from zhconv import convert as cv
from urllib.request import urlopen
from xlwt import Workbook

def pachong2(): #爬取每个曲谱的代码
    global title
    url1 = 'https://gongchepu.net/list/published/'  # input('url?')
    html = urlopen(
        url1
    ).read().decode('utf-8')
    pat1=re.compile(r'/reader/\d\d\d+/')
    match1 = re.findall(pat1, html)

    print(match1)
    #print(html)
    file= open('昆曲曲谱代码.txt','w')
    for i in match1:
        file.write(i+'\n')
    file.close()

def qupu():
    zidict = {}
    file = open('昆曲曲谱代码.txt', 'r')
    dirclist=file.readlines()

    ##

    for dirc in dirclist:
        print(dirc)

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

    print(zidict)
    with open('字频.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile,encoding='utf-8-sig')
        for key, value in zidict.items():
            print(key,value)
            writer.writerow([key,value])

def jiantuan():
    csvFile = open("字频.csv", "rb")
    reader = unicodecsv.reader(csvFile,encoding='utf-8-sig')
    zidict = []
    for item in reader:

        zidict.append(item)

    a=sorted(zidict, key=lambda x: int(x[1]), reverse=True)

    t500=np.array(a[0:500])
    t1000=np.array(a[0:-1])
    global jianzi
    global duoyinzi
    global rushengzi
    jianzi = open('jianzi.txt', 'r', encoding='utf-8-sig').read()
    duoyinzi = open('duoyinzi.txt', 'r', encoding='utf-8-sig').read()
    rushengzi = open('rusheng.txt', 'r', encoding='utf-8-sig').read()

    def isjian(cha):

        if cha in jianzi and i in duoyinzi:
            return('多')
        elif cha in jianzi:
            return('尖')
        else:
            return('团')
    def isru(cha):

        if cha in rushengzi:
            return ('入声')
        else:
            return('非入')

    wb = Workbook()
    st1=wb.add_sheet('入声及尖团')
    st1.write(0, 0, '昆曲入声及尖团字统计，计频率前800')
    st1.write(1,0,'顺序')
    st1.write(1,1,'字')
    st1.write(1, 2, '尖团')
    st1.write(1, 3, '声调')
    st1.write(1, 4, '频率(%)')


    st2 = wb.add_sheet('尖团')
    st2.write(0, 0, '昆曲尖团字统计，计频率前300')
    st2.write(1, 0, '顺序')
    st2.write(1, 1, '字')
    st2.write(1, 2, '频率(%)')



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

        if isjian(i)=='团'and isru(i)=='非入' :
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
                print(i,isjian(i),isru(i),'频率',round(freq,2))

        if isjian(i)=='尖'and n2<301:
            st2.write(n2 + 1, 0, n2)
            st2.write(n2+1, 1, i)

            if round(freq,2)==0:
                st2.write(n2 + 1, 2,'<0.01')
            else:
                st2.write(n2+1, 2, round(freq,2))
            n2+=1

        if isru(i)=='入声'and n3<501:
            st3.write(n3 + 1, 0, n3)
            st3.write(n3+1, 1, i)

            if round(freq,2)==0:
                st3.write(n3 + 1, 2,'<0.01')
            else:
                st3.write(n3+1, 2, round(freq,2))
            n3+=1



    wb.save('昆曲入声及尖团统计.xls')

def jiantuan2(): #尖团字表转换
    jian=open('jian.txt','r',encoding='utf-8-sig')
    jianzi=jian.read()
    pat2 = re.compile(r"[\u4e00-\u9fa5]")
    jianzi= str(re.findall(pat2,jianzi))
    jianzi = re.sub('\'|,| |\[|\]', '', jianzi)
    #print(i)
    jian2=open('jianzi.txt','w',encoding='utf-8-sig')
    jian2.write(jianzi)
    jian.close()
    jian2.close()
    duoyin=open('multi.txt','r',encoding='utf-8-sig')
    duoyinzi=duoyin.read()
    duoyinzi = str(re.findall(pat2, duoyinzi))
    duoyinzi = re.sub('\'|,| |\[|\]', '', duoyinzi)
    duoyin2=open('duoyinzi.txt','w',encoding='utf-8-sig')
    duoyin2.write(duoyinzi)
    duoyin.close()
    duoyin2.close()
    ru=open('ru.txt','r',encoding='utf-8-sig').read()
    rusheng = str(re.findall(pat2, ru))
    rushengzi = re.sub('\'|,| |\[|\]', '', rusheng)
    rushengzi2=open('rusheng.txt','w',encoding='utf-8-sig')
    rushengzi.join(set(rushengzi))
    rushengzi2.write(rushengzi)
    rushengzi2.close()

#执行顺序
#pachong2()已经有了
#jiantuan2()也有了
qupu()#字频统计
jiantuan()#尖团，入声分析
