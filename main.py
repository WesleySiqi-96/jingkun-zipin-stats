def pachong():
    import codecs
    from urllib.request import urlopen
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
    print(gongchepu)
    file=codecs.open(title+'.txt','w','utf-8')
    for i in gongchepu:
        file.write(i+"\n")
    file.close
pachong()