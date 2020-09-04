import codecs
import matplotlib.pyplot as p
import matplotlib as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.path import Path
from urllib.request import urlopen
def pachong():
    global title
    url1='https://gongchepu.net/reader/215/'#input('url?')
    title='彈詞'

         #input('标题？')
    # if has Chinese, apply decode()
    html = urlopen(
        url1
    ).read().decode('utf-8')
    html=html.split('\r\n')
    start=html.index('#'+title)
    endline=html[-1]
    endline=endline[0:endline.find('</div>')]
    gongchepu=html[start:-1]+[endline]
    #print(gongchepu)
    file=codecs.open(title+'.txt','w','utf-8')
    for i in gongchepu:
        file.write(i+"\n")
    file.close


def plotsan():
    plt.rcParams['font.family'] = 'KaiTi'
    pu=codecs.open('彈詞'+'.txt','r','utf-8')
    fig,ax=p.subplots(figsize=(8.5,11))
    p.ylim(0,1)
    p.xlim(0,1)
    hang=0
    lie=0
    DD=['上調','尺調','小工調','凡調','六調','正宮調','上调','尺调','小工调','凡调','六调','正宫调']
    Ddict={'上調':'1=bB','尺調':'1=C','小工調':'1=D','凡調':'1=bE','六調':'1=F','正宮調':'1=G',
'上调':'1=bB','尺调':'1=C','小工调':'1=D','凡调':'1=bE','六调':' 1=F','正宫调':'1=G'}
    gcdict={'合':'-5','四':'-6','一':'-7','上':'1','尺':'2','工':'3','凡':'4','六':'5','五':'6','乙':'7'}
    gclist=['合','四','一','上','尺','工','凡','六','五','乙']
    for line in pu:
        line.replace('\n','')
        if any(diaomen in line for diaomen in DD):
            for diaomen in DD:
                if diaomen in line:
                    D=diaomen+'，'+Ddict[diaomen]
        elif line[0]=='#': #標題
            lie = 0.5
            p.text(0.5,1,line[1:-1], horizontalalignment='center',size=36)
            hang+=1
            if hang > 20:
                #p.axis('off')
                fig=p.figure(2, figsize=(8.5, 11), dpi=100)
                p.ylim(0, 1)
                p.xlim(0, 1)
                hang = 0
        elif line[0]=='【':
            qupai=line.replace('\n', '')
            p.text(lie / 20, 1 - hang / 20, qupai+'（'+D+'）', horizontalalignment='left', size=15)
            hang += 1
            if hang > 20:
                #p.axis('off')
                fig=p.figure(2, figsize=(8.5, 11), dpi=100)
                p.ylim(0, 1)
                p.xlim(0, 1)
                hang = 0
        elif line[0:4]=='&gt;': #夾白
            lie = 0.5
            p.text(lie/20,1-hang/20, line[4:-1], horizontalalignment='left', size=15)
            hang+=1
            if hang > 20:
                #p.axis('off')
                fig=p.figure(2, figsize=(8.5, 11), dpi=100)
                p.ylim(0, 1)
                p.xlim(0, 1)
                hang = 0
        elif line[0]=='=':#念白
            lie = 0.5
            num =1
            while num<len(line):
                if num ==1:
                    p.text(lie / 20, 1 - hang / 20, '（念）'+line[num:num + 27].replace('\n', ''), multialignment='left',size=15)
                    num += 27
                else:
                    p.text(lie/20,1-hang/20, line[num:num+30].replace('\n',''), multialignment='left', size=15)
                    num+=30
                aa=line[num:num+30]
                hang += 1
                if hang > 20:
                    #p.axis('off')
                    fig=p.figure(2, figsize=(8.5, 11), dpi=100)
                    p.ylim(0, 1)
                    p.xlim(0, 1)
                    hang = 0
        elif  line[0:3]=='\pz':
            pass
        else: #唱
            p.text(lie / 20, 1 - (hang+1) / 20, line[0], horizontalalignment='center', size=15)
            gcnum=0
            for i in line:
                if i in gclist: #数工尺
                    gcnum+=1

            if gcnum==1:
                for gc in line[1:-1]:
                    if gc in gcdict: #在此加 腔&高低音
                        if int(gcdict[gc])>0:
                            p.text(lie / 20, 1 - hang / 20, gcdict[gc], horizontalalignment='center', size=15)
                        elif int(gcdict[gc])<0:
                            p.text(lie / 20, 1 - hang / 20, str(-int(gcdict[gc])), horizontalalignment='center', size=15)
                            p.text((lie+0.1) / 20, 1 - (hang+0.3) / 20, '.', horizontalalignment='center', size=20)
                        lie+=1
            elif gcnum==2:
                for gc in line[1:-1]:
                    if gc in gcdict:
                        if int(gcdict[gc]) > 0:
                            p.text(lie / 20, 1 - hang / 20, gcdict[gc], horizontalalignment='center', size=15)
                        elif int(gcdict[gc]) < 0:
                            p.text(lie / 20, 1 - hang / 20, str(-int(gcdict[gc])), horizontalalignment='center',
                                   size=15)
                            p.text((lie + 0.1) / 20, 1 - (hang + 0.3) / 20, '.', horizontalalignment='center', size=20)
                        lie += 0.7
                        #p.show()
                p.hlines(y=1 - (hang + 0.1) / 20, xmin=(lie-1.2 ) / 10, xmax=(lie-1.8 ) / 10, colors='black')
                arc=plt.patches.Arc(((lie-1.05) / 20, 1 - (hang-0.2) / 20),1.3/20,1/20,theta1=30,theta2=150)
                ax.add_patch(arc)



            elif gcnum==3:
                pass

            elif gcnum==4:
                pass

            elif gcnum==5:
                pass

            elif gcnum==6:
                pass

            if lie>20:
                lie=0.5
                hang+=2
                if hang>20:
                    #p.axis('off')
                    fig=p.figure(figsize=(8.5,11),dpi=100)
                    p.ylim(0, 1)
                    p.xlim(0, 1)
                    hang=0
            #p.text(lie/20,1-(hang-1)/20,plot,horizontalalignment='left', size=15)



    #p.axis('off')
    #p.savefig('1',dpi=300)
    p.show()

plotsan()
