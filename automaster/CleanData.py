# -*- coding:utf-8 -*-
import pandas as pd
import re


# 数据清洗
class CleanData:
    # 要去除的固定词
    unUselessWords = ['[语音]', '[图片]']
    unUselessSymbol = '[`~!@#$^&*()_\\-+=|{}\':;\',\\[\\]<>/?~！@#￥……&*（）——+|{}【】‘；：”“’。，、？]'
    web_reg = r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    taobao_reg = r"￥[A-Za-z0-9]+￥"

    @staticmethod
    def cleanData(string):
        # 去除无用关键词
        string = CleanData.removeUselessWords(string)
        # 去除网址
        string = CleanData.removeWeb(string)
        # 去除淘口令
        string = CleanData.removeTaobao(string)
        # 去除特殊符号保留 符号.
        string = CleanData.removeSymbols(string)
        return string

    @staticmethod
    def removeUselessWords(string):
        for word in CleanData.unUselessWords:
            if (word in string):
                string = string.replace(word, ' ')
        return string

    # 去除网址
    @staticmethod
    def removeWeb(string):
        pattern = re.compile(CleanData.web_reg)
        return pattern.sub(" ", string)

    # 去除手淘链接例如 ￥orIk0ITYkCs￥
    @staticmethod
    def removeTaobao(string):
        pattern = re.compile(CleanData.taobao_reg)
        return pattern.sub("", string)

    # 去除特殊符号 ? ,| 等但是保留. %
    @staticmethod
    def removeSymbols(string):
        pattern = re.compile(CleanData.unUselessSymbol)
        return pattern.sub(" ", string)


if __name__ == '__main__':
    string = '技师说：您好，蓄电池亏电严重，需要拆下蓄电池小电流充电，最佳。例如45安时，10安培电流充电4.5小时SOC100%，此时充电完毕。电压不低于12.6伏'
    print(CleanData.cleanData(string))
