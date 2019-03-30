# coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import os
import pickle
from tqdm import tqdm
import re


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
                count_dic[state] = 0

        def makeLabel(text):
            out_text = []
            if len(text) == 1:
                out_text.append('S')
            else:
                out_text += ['B'] + ['M'] * (len(text) - 2) + ['E']
            return out_text

        init_parameters()
        line_num = -1

        with open(path, encoding='utf8') as f:
            for line in tqdm(f.readlines()):
                line_num += 1
                line = line.strip()
                if not line:
                    continue
                word_list = [char for char in line if char != ' ']
                line_list = line.split()
                line_state = []
                for word in line_list:
                    line_state.extend(makeLabel(word))
                assert len(line_state) == len(word_list)

                for k, v in enumerate(line_state):
                    if k < (len(line_state) - 1):
                        count_dic[v] += 1.0
                        # 统计状态转移的总数，除开最后一个字没有转移

                    self.B_dic[v][word_list[k]] = \
                        self.B_dic[v].get(word_list[k], 0) + 1.0
                    if k == 0:
                        self.Pi_dic[v] += 1
                    else:
                        self.A_dic[line_state[k - 1]][v] += 1.0

        # 根据频度计算概率
        self.Pi_dic = {k: v * 1.0 / line_num for k, v in self.Pi_dic.items()}

        # 用于计算发射概率。记录每个隐藏状态发射到词的总数
        sum_of_B_dic = {}
        for state, word_count in self.B_dic.items():
            sum_of_B_dic[state] = sum(v for k, v in word_count.items())

        # 拉普拉斯平滑，分子加一，分母加 分子个数*1
        self.B_dic = {state: {word: (count + 1) / (sum_of_B_dic[state] + len(word_count.items()))
                              for word, count in word_count.items()}
                      for state, word_count in self.B_dic.items()}

        self.A_dic = {k: {k1: v1 / count_dic[k] for k1, v1 in v.items()}
                      for k, v in self.A_dic.items()}

        with open(self.model_file, 'wb') as f:
            pickle.dump(self.A_dic, f)
            pickle.dump(self.B_dic, f)
            pickle.dump(self.Pi_dic, f)

        return self

    def viterbi(self, text, states, start_p, trans_p, emit_p):
        """
        维特比算法，用于根据观测序列推测最有可能的隐藏状态序列。
        到达第t步第n状态的最优路径，需要计算前t-1的全部路径到第n状态的最优路径，则计算出t时刻的一条路径
        这里概率最大的路径就是最优路径
        :param text: 观测序列
        :param start_p: 初始概率向量,PI_dict
        :param trans_p: 状态转移概率矩阵
        :param emit_p: 发射概率矩阵,B_dict
        :return: 对应观测序列的最有可能的隐藏状态序列
        """
        # 列表由字典组成，每个字典保存从起点到该时刻的所有状态的最大概率
        V = [{}]
        path = {}  # 从起点到时刻t各个状态的最优路径
        # 初始化,求第一个词发射（观测）的可能
        for y in states:
            V[0][y] = start_p[y] * emit_p[y].get(text[0], 0)
            path[y] = [y]
        # {'E': ['E'], 'B': ['B'], 'M': ['M'], 'S': ['S']}

        for t in range(1, len(text)):
            V.append({})  # 用于保存当前时刻各个状态的概率
            new_path = {}  # 用于保存从起点到当前时刻各个状态的最优路径

            # 检验发射概率矩阵中是否有这个字
            never_seen = (text[t] not in self.B_dic['S'].keys()) and \
                         (text[t] not in self.B_dic['B'].keys()) and \
                         (text[t] not in self.B_dic['M'].keys()) and \
                         (text[t] not in self.B_dic['E'].keys())

            for y in states:
                # 计算状态y的发射概率,未登陆词默认全部状态的发射概率为1
                emit_P = emit_p[y].get(text[t], 0) if not never_seen else 1.0
                # 遍历前一时刻的所有状态。从前一时刻所有可达状态(概率大于0)出发
                # V[t - 1][y0]上次路径得分值， trans_p[y0].get(y, 0)转移概率，emit_P发射概率
                prob, state = max([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_P, y0)
                                   for y0 in states if V[t - 1][y0] > 0])
                # for y0 in states:
                #     if V[t - 1][y0] > 0:
                #         print((V[t - 1][y0] * trans_p[y0].get(y, 0)* emit_P, y0))

                V[t][y] = prob  # 从起点到t时刻状态y的最大概率为prob
                # t时刻状态y的最优路径是从前一时刻状态state的路径出发到当前时刻
                new_path[y] = path[state] + [y]

            # 每个出发点追加其最佳的下一步路径，new_path[y]始终记录，改出发点的路径更新
            # path[state] 为上一步的路径
            path = new_path  # 为从起点到终点时刻各个状态的最优路径
        # {'S': ['B', 'E', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S'], 'E': ['B', 'E', 'S', 'B', 'E', 'B', 'E', 'S', 'S', 'E'], 'B': ['B', 'E', 'S', 'B', 'E', 'B', 'E', 'S', 'S', 'B'], 'M': ['B', 'E', 'S', 'B', 'E', 'B', 'E', 'S', 'S', 'M']}

        # 找出最优路径：对比终点时刻的各个状态对应的最优路径的概率，概率最大的
        # 状态就是终点应该到达的状态，对应的路径就是全局最优路径
        prob, state = max([V[len(text) - 1][y], y] for y in self.state_list)
        return prob, path[state]

    def cut(self, text):
        if not self.load_para:
            self.try_load_model(os.path.exists(self.model_file))

        prob, pos_list = self.viterbi(text, self.state_list, self.Pi_dic, self.A_dic, self.B_dic)
        begin, next_pos = 0, 0
        for i in range(len(text)):
            pos = pos_list[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                yield text[begin: i + 1]
                next_pos = i + 1
            elif pos == 'S':
                yield text[i]
                next_pos = i + 1
        if next_pos < len(text):
            yield text[next_pos:]


if __name__ == '__main__':
    hmm = HMM()
    # hmm.train('../data/train_.txt')
    # print(hmm.A_dic)
    re_han_cut_all = re.compile("([\u4E00-\u9FD5]+)", re.U)

    str = "销售类人才需求量大，是由岗位本身特点所致。重庆智成人才市场相关负责人介绍，一方面企业需要优秀的销售人员推动产品的市场份额，这类人才不可或缺。另一方面，销售类岗位工作地点及收入相对不稳定，工作压力大，导致人员流动性强。加之部分高校毕业生不愿从基层销售工作干起，造成销售类岗位供需比例不平衡。"

    lines = re_han_cut_all.split(str)
    for line in re_han_cut_all.split(str):
        # print(line)
        print(list(hmm.cut(line)))
    # print(list(hmm.cut('重庆智成人才市场相关负责人介绍，一方面企业需要优秀的销售人员推动产品的市场份额，这类人才不可或缺。另一方面，销售类岗位工作地点及收入相对不稳定，工作压力大，导致人员流动性强。加之部分高校毕业生不愿从基层销售工作干起，造成销售类岗位供需比例不平衡。')))
