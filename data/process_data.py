#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import re
from tqdm import  tqdm
f1 = open('train_.txt','w',encoding='utf8')
with open('2014_corpus.txt','r',encoding='utf8') as f:
    lines = f.readlines()
    for line in tqdm(lines):
        line = line.strip()
        line = re.sub(r'/[A-Za-z]{1,5}','',line)
        line = re.sub(r'。 ','。 \n',line)
        f1.write(line)


        # f1.write(line)
        # for sub_line in line.split('。'):
        #     # print(sub_line)
        #     f1.write(sub_line+'。'+'\n')
#

# str = 'abcad。asdjao。asa'
# print(str.split('。'))