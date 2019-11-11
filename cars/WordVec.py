import pandas as pd
import jieba

# 将数据转化为向量形式
from cars.CleanData import CleanData


class WordVec:
    trainData = 'datas/AutoMaster_TrainSet.csv'
    testData = 'datas/AutoMaster_TestSet.csv'
    stopWords = 'datas/stopwords.txt'

    @staticmethod
    def cut(string):
        return jieba.cut(string)

    @staticmethod
    def get_stopwords_list(path):
        stopwords = [line.strip() for line in open(path, encoding='UTF-8').readlines()]
        return stopwords

    @staticmethod
    def remove_stop_words(list):


    # 获取数据
    @staticmethod
    def getAllText(path):
        dataFrame = pd.read_csv(WordVec.trainData, encoding="UTF-8")
        # 获取所需列
        dataFrame = dataFrame.iloc[:, 1:6]
        # 将所有列拼接成一个list
        text_list = []
        for index, row in dataFrame.iteritems():
            text_list.extend(dataFrame[index].tolist())

        # 清洗数据
        text_list = [CleanData.cleanData(str(a)) for a in text_list]

        text = ''
        for a in text_list:
            text += a
            text += ' '


if __name__ == '__main__':
    # WordVec.getAllText(WordVec.trianData)
    # string = '我这边2017年9月23号买了一辆斯科达的科迪亚克7座豪华USV，2028年1月14号首保发现漏油4S店说是齿轮防锈油，用纸擦了一'
    # string = CleanData.cleanData(string)
    # cut_list = WordVec.cut(string)
    # for item in cut_list:
    #     print(item)
    print(type(WordVec.get_stopwords_list(WordVec.stopWords)))
