jianzi = open('./data/尖字表.txt', 'r', encoding='utf-8-sig').read()
duoyinzi = open('./data/多音字表.txt', 'r', encoding='utf-8-sig').read()
jqxhanzi =open('./data/jqx汉字.txt', 'r', encoding='utf-8-sig').read()
rushengzi = open('./data/入声字表.txt', 'r', encoding='utf-8-sig').read()


def isjian(cha):
    if cha in jianzi and cha in duoyinzi:
        return ('多')
    elif cha in jianzi:
        return ('尖')
    elif cha in jqxhanzi:
        return ('团')
    else:
        return ('非')


def isru(cha):
    if cha in rushengzi:
        return ('入声')
    else:
        return ('非入')