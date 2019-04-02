# coding: utf-8
"""
@author: linwenxing
@contact: linwx.mail@gmail.com
"""
import os


def tag_line(words):
    chars = []
    tags = []
    temp_word = ''  # 用于合并组合词
    for word in words:
        # print(word)
        word = word.strip('\t ')
        if temp_word == '':
            bracket_pos = word.find('[')
            try:
                w, h = word.split('/')
            except Exception as e:
                if word == '//w':
                    w = '/'
                    h = '/w'
                elif word.endswith('/m'):
                    w = word[:-2]
                    h = '/m'
                else:
                    w = ''
                    h = ''
            if bracket_pos == -1:
                if len(w) == 0: continue
                chars.extend(w)
                if h.startswith('ns'):
                    tags += ['S'] if len(w) == 1 else ['B'] + ['M'] * (len(w) - 2) + ['E']
                else:
                    tags += ['O'] * len(w)
            else:
                w = w[bracket_pos + 1:]
                temp_word += w
        else:
            bracket_pos = word.find(']')

            try:
                w, h = word.split('/')
            except Exception as e:
                if word == '//w':
                    w = '/'
                    h = '/w'
                elif word.endswith('/m'):
                    w = word[:-2]
                    h = '/m'
                else:
                    w = ''
                    h = ''
            if bracket_pos == -1:
                temp_word += w
            else:
                w = temp_word + w
                h = word[bracket_pos + 1:]
                temp_word = ''
                if len(w) == 0: continue
                chars.extend(w)
                if h.startswith('ns'):
                    tags += ['S'] if len(w) == 1 else ['B'] + ['M'] * (len(w) - 2) + ['E']
                else:
                    tags += ['O'] * len(w)

    assert temp_word == ''
    return (chars, tags)



def read_line(data_path):
    root = os.path.dirname(data_path)
    with open(data_path) as data_file, \
            open(os.path.join(root, 'train_.txt'), 'w') as train_file, \
            open(os.path.join(root, 'test_.txt'), 'w') as test_file:
        count_num = 0
        for line in data_file:
            line = line.strip('\r\n\t ')
            if line == '':
                continue
            is_test = True if count_num % 5 == 0 else False
            words = line.split()
            if len(words) == 0:
                continue
            line_chars, line_tags = tag_line(words)
            save_file = test_file if is_test else train_file
            for k, v in enumerate(line_chars):
                save_file.write(v + '\t' + line_tags[k] + '\n')
            save_file.write('\n')
            count_num += 1

if __name__ == '__main__':
    read_line('../CRF_data/data.txt')