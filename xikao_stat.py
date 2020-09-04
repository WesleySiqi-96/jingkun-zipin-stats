import codecs
import re
import unicodecsv
import numpy as np
import matplotlib.pyplot as p
import matplotlib as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.path import Path
from urllib.request import urlopen
import xlwt
from xlwt import Workbook
import os


def pachong2():
    global title
    url1 = 'http://scripts.xikao.com/list/comprehensive'  # input('url?')
    html = urlopen(
        url1
    ).read().decode('utf-8')
    pat1=re.compile(r'/play/\d+')
    match1 = re.findall(pat1, html)

    match1=list(set(match1))
    file= open('xikao123.txt','w')
    for i in match1:
        file.write(i+'\n')
    file.close()

def juben():

    zidict = {}
    file = open('xikao123.txt', 'r')
    dirclist = file.readlines()
    for dirc in dirclist:
        try:
            print(dirc)

            url1='http://scripts.xikao.com'+dirc
            html = urlopen(
                url1
            ).read().decode('utf-8')
            pat2=re.compile(r"全剧剧本：纯文本格式.+<br /><br />")
            i=str(re.findall(pat2,html))

            pu = re.sub('<br /><p>\S+?\\\\u3000\\\\',"", i)
            pu = re.sub('</p><p>\S+?\\\\u3000\\\\', "", pu)
            pu = re.sub('<br />|</b>|\\\\u3000|u3000|[【](.*?)[】]|[（](.*?)[）]|</p>|<p>', "",pu)
            pu = re.sub('<span.+span>', "",pu)
            pu= re.sub('全剧剧本：纯文本格式',"", pu)

            pu = re.sub('=|。|，|、|……|；|#|&|"|“|”|;|,|？|！|!|\?|﻿：|：|\u2026|/.|《|》', '', pu)
            title=re.findall(re.compile(r"\d+"),dirc)
            file = open('C:/Users/wesley/Google drive/Sync/京昆/pdf/昆/简谱/python/xikao/'+
                        str(title)[2:-2]+'.txt', 'w')
            file.write(str(pu[2:-2]))
            file.close()
        except:
            pass

        # for zi in pu:
        #     if zi in zidict:
        #         zidict[zi]+=1
        #     else:
        #         zidict[zi]=1
def statss():
    zidict = {}
    allf=os.listdir('C:/Users/wesley/Google drive/Sync/京昆/pdf/昆/简谱/python/xikao/')
    for name in allf:
        file = open('C:/Users/wesley/Google drive/Sync/京昆/pdf/昆/简谱/python/xikao/' + name, 'r')
        f=[]
        f=file.read()
        for cha in f:
            if cha in zidict:
                zidict[cha] += 1
            else:
                zidict[cha] = 1
        file.close()
    with open('戏考字频.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile, encoding='utf-8-sig')
        for key, value in zidict.items():
            print(key, value)
            writer.writerow([key, value])

    print(zidict)

def jianzi2():
    csvFile = open("戏考字频.csv", "rb")
    reader = unicodecsv.reader(csvFile, encoding='utf-8-sig')
    zidict = []
    for item in reader:
        zidict.append(item)

    a = sorted(zidict, key=lambda x: int(x[1]), reverse=True)
    t1000 = np.array(a[0:-1])
    global jianzi
    global duoyinzi
    jianzi = open('jianzi.txt', 'r', encoding='utf-8-sig').read()
    duoyinzi = open('duoyinzi.txt', 'r', encoding='utf-8-sig').read()
    def isjian(cha):

        if cha in jianzi and i in duoyinzi:
            return('多')
        elif cha in jianzi:
            return('尖')
        else:
            return('团')

    wb = Workbook()
    st1 = wb.add_sheet('尖团')
    st1.write(0, 0, '京剧尖团字统计，计频率前300')
    st1.write(1, 0, '顺序')
    st1.write(1, 1, '字')
    st1.write(1, 2, '频率(%)')

    n1=1
    for count in range(len(t1000[:,0])):
        freq=int(t1000[count,1])/np.sum(t1000[:,1].astype(float))*100
        i=t1000[count,0]

        if isjian(i) == '尖' and n1 < 301:
            st1.write(n1 + 1, 0, n1)
            st1.write(n1 + 1, 1, i)

            if round(freq, 2) == 0:
                st1.write(n1 + 1, 2, '<0.01')
            else:
                st1.write(n1 + 1, 2, round(freq, 2))
            n1 += 1

    wb.save('京剧尖团统计.xls')
jianzi2()