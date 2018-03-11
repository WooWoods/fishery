#!-*- coding:utf-8 -*-
import sys
import re

keys = {
        '种名':     'fishname',
        '学名':     'latin_name',
        '别名':     'other_names',
        '目'  :     'order',
        '科'  :     'family',
        '属'  :     'genus',
        '濒危等级': 'level',
        'pic':      'pic',
        '主要性状': 'feature',
        '生活习性': 'habit',
        '食性':     'foods',
        '生殖':     'reproduce',
        '年龄和生长':'growth',
        '分布':     'distribution',
        '经济意义': 'commercial',
        '致危原因': 'danger_reason',
        '驯养繁殖状况': 'domescation',
        '现有保护': 'protection',
        '建议采取措施': 'protection_sugession',
        '估计数量': 'quantity',
        '致危因素及现状': 'danger_reason'
        }


def load_data(f):
    fishes = []
    titles = '主要性状,生活习性,食性,生殖,年龄和生长,分布,经济意义,致危原因,驯养繁殖状况,现有保护,建议采取措施,估计数量,致危因素及现状'.split(',')
    new_fish = False
    lines = []
    dic = {}
    for line in file(f):
        text_line = False
        if re.match(r'^\s$', line):
            continue
        line = line.strip()
        if re.match(r'种名', line):
            if dic:
                # if lines:
                    # dic[key] = ''.join(lines)
                fishes.append(dic)
            dic = {}
            arr = line.split(':')
            key = keys.get(arr[0])
            dic[key] = arr[1]
            continue
        if re.search(r':', line):
            arr = line.split(':')
            key = keys.get(arr[0])
            dic[key] = arr[1]
        else:
            if line in titles:
                text_line = True
                if lines:
                    dic[key] = ''.join(lines)
                lines = []
                key = keys.get(line)
                # continue
            # if text_line:
            else:
                lines.append(line)

    fishes.append(dic)
    return fishes

def output(fishes):
    with open('output.txt', 'w') as fh:
        for r in fishes:
            for k in r:
                fh.write('%s\t\t%s\n' %(k, r[k]))
            fh.write('\n')


if __name__ == '__main__':
    f = sys.argv[1]
    fishes = load_data(f)
    output(fishes)


