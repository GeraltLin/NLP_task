#coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
str = "销售类人才需求量大，是由岗位本身特点所致。重庆智成人才市场相关负责人介绍，一方面企业需要优秀的销售人员推动产品的市场份额，这类人才不可或缺。另一方面，销售类岗位工作地点及收入相对不稳定，工作压力大，导致人员流动性强。加之部分高校毕业生不愿从基层销售工作干起，造成销售类岗位供需比例不平衡。"

import jieba
print(list(jieba.cut(str)))
