import pandas as pd
import jieba

# 将数据转化为向量形式
from automaster.CleanData import CleanData
from automaster.utils import config


class WordVec:
    trainData = 'datas/AutoMaster_TrainSet.csv'
    testData = 'datas/AutoMaster_TestSet.csv'
    stopWords = 'datas/stopwords.txt'
    vocabToInt = 'datas/VocabToInt.txt'

    def cut(self, string):
        return jieba.cut(string)

    def get_stopwords_list(self, path):
        stopwords = [line.strip() for line in open(path, encoding='UTF-8').readlines()]
        return stopwords

    # 去除通用词
    def remove_stop_words(self, text):
        return [t for t in text if
                t.strip() and t not in self.get_stopwords_list(WordVec.stopWords)]

    # 去除空格
    def remove_space(self, text):
        return [t for t in text if t.strip()]

    def get_vocab(self, texts):
        vocab_set = set(texts)
        vocab_to_int = {word: index for index, word in enumerate(vocab_set)}
        with open(WordVec.vocabToInt, 'w+', encoding='UTF-8') as f:
            for k, v in vocab_to_int.items():
                f.write(str(k) + ' ' + str(v) + '\n')
        return vocab_to_int

    # 获取数据
    def get_vocab_data(self, path):
        dataFrame = pd.read_csv(WordVec.trainData, encoding="UTF-8")
        # 获取所需列
        dataFrame = dataFrame.iloc[:, 1:6]

        dataFrame2 = pd.read_csv(WordVec.testData, encoding="UTF-8")
        # 获取所需列
        dataFrame2 = dataFrame.iloc[:, 1:5]
        # 将所有列拼接成一个list
        text_list = []
        for index, row in dataFrame.iteritems():
            text_list.extend(dataFrame[index].tolist())
        for index, row in dataFrame2.iteritems():
            text_list.extend(dataFrame2[index].tolist())
        # 清洗数据
        print('清洗数据')
        text_list = [CleanData.cleanData(str(a)) for a in text_list]

        # 拼接所有字符串
        print('拼接所有字符串')
        text = ''
        for a in text_list:
            text += a
            text += ' '

        # 切词
        print('切词')
        cut_text = self.cut(text)

        # 去除空格
        print('去除空格')
        valid_text = self.remove_space(cut_text)

        # 生成词表文件
        print('生成词表文件')
        self.get_vocab(valid_text)

    @staticmethod
    def get_data_frame(test_data_path, train_data_path):
        train_data_frame = pd.read_csv(config.train_data_path, encoding="UTF-8")
        test_data_frame = pd.read_csv(config.test_data_path, encoding="UTF-8")
        return train_data_frame, test_data_frame

    # 处理string 将其处理成所需形式
    # 去除特殊符号，链接，淘口令等
    @staticmethod
    def process_sentence(string):
        pass

    # 根据Brand Model 两列生成userdict,优化切词
    @staticmethod
    def get_user_dict(train_data_frame, test_data_frame):
        data = []
        data.extend(train_data_frame['Brand'].to_list())
        data.extend(train_data_frame['Model'].to_list())
        data.extend(test_data_frame['Brand'].to_list())
        data.extend(test_data_frame['Model'].to_list())
        user_dict_set = set(data)
        with open(config.user_dict, 'w', encoding="UTF-8") as file:
            for user in user_dict_set:
                file.write(user + '\n')


if __name__ == '__main__':
    wordVec = WordVec()
    # wordVec.get_vocab_data(WordVec.trainData)
    wordVec.get_data_frame()