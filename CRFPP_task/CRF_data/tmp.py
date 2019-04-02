#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import re
with open('2014_corpus.txt',encoding='utf8') as fr, open('data.txt','w') as fw:
    for line in fr:
        line  = line.strip('\r\n\t ')
#
        line = re.sub(r'](/)([a-zA-Z]+)', '] \g<2>', line)
        print(line)
        fw.write(line+'\n')

# # print('//w'.split('/'))
# line = '人民网/nz 1月1日/t 讯/ng 据/p 《/w [纽约/nsf 时报/n]/nz 》/w'
#
# line = re.sub(r'](/)([a-zA-Z]+)', '] \g<2>', line)

