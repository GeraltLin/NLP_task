#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
from WordSegmentation import MM,RMM

class BIMM(object):
    """
    双向最大匹配
    """
    def __init__(self, dic_path):
        self.dictionary = set()
        self.maximum = 0
        # 读取词典
        with open(dic_path, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)


    def MM_cut(self, text):
        result = []

        curLen = len(text)
        index= 0
        while curLen > 0:
            word = None
            # size 从词典中最大长度开始算
            for size in range(self.maximum, 0, -1):
                if curLen - size < 0:
                    continue
                #匹配字段
                piece = text[index:index+size]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    #匹配到了从将原句中移除头端的词语
                    index += size
                    curLen -=size
                    break
            #词典中没有任何匹配信息，则缩短原句
            if word is None:
                index += 1
                curLen -=1
        return result

    def RMM_cut(self, text):
        result = []

        index = len(text)
        while index > 0:
            word = None
            # size 从词典中最大长度开始算
            for size in range(self.maximum, 0, -1):
                if index - size < 0:
                    continue
                #匹配字段
                piece = text[(index - size):index]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    #匹配到了从将原句中移除尾端的词语
                    index -= size
                    break
            #词典中没有任何匹配信息，则缩短原句
            if word is None:
                index -= 1
        return result[::-1]


    def cut(self, text):
        RMM_reselt = self.RMM_cut(text)
        MM_reselt = self.MM_cut(text)
        if len(RMM_reselt)<=len(MM_reselt):
            return RMM_reselt
        else:
            return MM_reselt


if __name__ == '__main__':
    text = "南京市长江大桥66"

    tokenizer = BIMM('../data/imm_dic.utf8')
    print(tokenizer.cut(text))
