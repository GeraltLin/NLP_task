# coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import os
import pickle


class HMM(object):
    """
    A_dic：状态转移矩阵
    B_dic：观测概率矩阵
    Pi_dic：初始分布
    B:begin
    M:middle
    E:end
    S:single
    """

    def __init__(self):
        self.model_file = '../data/hmm_model.pkl'
        self.state_list = ['B', 'M', 'E', 'S']
        self.load_para = False

    def try_load_model(self, trained):
        if trained:
            with open(self.model_file, 'rb') as f:
                self.A_dic = pickle.load(f)
                self.B_dic = pickle.load(f)
                self.Pi_dic = pickle.load(f)
                self.load_para = True
        else:
            self.A_dic = {}
            self.B_dic = {}
            self.Pi_dic = {}
            self.load_para = False

    def train(self, path):
        self.try_load_model(False)
        count_dic = {}

        def init_parameters():
            for state in self.state_list:
                self.A_dic[state] = {s: 0.0 for s in self.state_list}
                self.Pi_dic[state] = 0.0
                self.B_dic[state] = {}

        def makeLabel(text):
            out_text = []
            if len(text) == 1:
                out_text.append('S')
            else:
                out_text += ['B'] + ['M'] * (len(text) - 2) + ['E']
            return out_text

        init_parameters()
        line_num = -1
        words = set()
        with open(path, encoding='utf8') as f:
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue
                word_list = [char for char in line if char != '']
                words |= set(word_list)
                line_list = line.split()
                line_state = []
                for word in line_list:
                    line_state.extend(makeLabel(word))


    def vertibi(self, text, states, strt_p, trans_p, emit_p):
        pass
