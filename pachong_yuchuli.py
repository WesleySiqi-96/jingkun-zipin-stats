from urllib.request import urlopen
import re


def pachong_kunqu(): #爬取每个曲谱的代码
    global title
    url1 = 'https://gongchepu.net/list/published/'  # input('url?')
    html = urlopen(
        url1
    ).read().decode('utf-8')
    pat1=re.compile(r'/reader/\d\d\d+/')
    match1 = re.findall(pat1, html)
    file= open('./data/昆曲曲谱代码.txt','w')
    for i in match1:
        file.write(i+'\n')
    file.close()

def pachong_xikao():
    global title
    url1 = 'http://scripts.xikao.com/list/comprehensive'  # input('url?')
    html = urlopen(
        url1
    ).read().decode('utf-8')
    pat1=re.compile(r'/play/\d+')
    match1 = re.findall(pat1, html)

    match1=list(set(match1))
    file= open('./data/戏考代码.txt','w')
    for i in match1:
        file.write(i+'\n')
    file.close()

def juben():
    file = open('./data/戏考代码.txt', 'r')
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
            file = open('./xikao/'+
                        str(title)[2:-2]+'.txt', 'w')
            file.write(str(pu[2:-2]))
            file.close()
        except:
            pass


def jiantuan_rusheng(): #尖团字表转换
    jian=open('./data/jian.txt','r',encoding='utf-8-sig')
    jianzi=jian.read()
    pat2 = re.compile(r"[\u4e00-\u9fa5]")
    jianzi= str(re.findall(pat2,jianzi))
    jianzi = re.sub('\'|,| |\[|\]', '', jianzi)
    #print(i)
    jian2=open('./data/尖字表.txt','w',encoding='utf-8-sig')
    jian2.write(jianzi)
    jian.close()
    jian2.close()
    duoyin=open('./data/multi.txt','r',encoding='utf-8-sig')
    duoyinzi=duoyin.read()
    duoyinzi = str(re.findall(pat2, duoyinzi))
    duoyinzi = re.sub('\'|,| |\[|\]', '', duoyinzi)
    duoyin2=open('./data/多音字表.txt','w',encoding='utf-8-sig')
    duoyin2.write(duoyinzi)
    duoyin.close()
    duoyin2.close()
    ru=open('./data/ru.txt','r',encoding='utf-8-sig').read()
    rusheng = str(re.findall(pat2, ru))
    rushengzi = re.sub('\'|,| |\[|\]', '', rusheng)
    rushengzi2=open('./data/入声字表.txt','w',encoding='utf-8-sig')
    rushengzi.join(set(rushengzi))
    rushengzi2.write(rushengzi)
    rushengzi2.close()

def jqx():
    url1 = 'http://xh.5156edu.com/pinyi.html'  # input('url?')
    html = urlopen(
        url1
    ).read().decode('ISO-8859-1')
    pat1 = re.compile(r'<a class=\'fontbox\'.+?>[jqx]')
    match1 = re.findall(pat1, html)

    pat2=re.compile(r'html2/[jqx]\d\d\.html')
    match2 = re.findall(pat2, ''.join(match1))
    hzlist=[]
    for item in match2:
        url2='http://xh.5156edu.com/'+item
        html2 = urlopen(
            url2
        ).read().decode('ANSI')
        pat3=re.compile(r'拼音</b></td><td width=86%><b>汉字.+</table><br></td>')
        pat4=re.compile(r"[\u4e00-\u9fa5]")
        match3=re.findall(pat3,html2)
        jqxhanzi=re.findall(pat4,str(match3[0][30:-1]))
        hzlist+=jqxhanzi
    file = open('./data/jqx汉字.txt', 'w')
    for i in hzlist:
        if i not in ['未','分','类']:
            file.write(i)
    file.close()

pachong_kunqu()
pachong_xikao()
juben()
jiantuan_rusheng()
#jqx()

