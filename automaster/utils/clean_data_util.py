import re


class CleanDataUtil:
    web_reg = r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    taobao_reg = r"￥[A-Za-z0-9]+￥"
    useless_symbol = r'[\s+\-\|\!\/\[\]\{\}_,.$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）]'
    useless_words = ['[语音]', '[图片]']

    # 清理数据
    @staticmethod
    def clean_sentence(sentence):
        if isinstance(sentence, str):
            # 去除网址
            sentence = CleanDataUtil.remove_web(sentence)
            # 去除淘口令
            sentence = CleanDataUtil.remove_taobao(sentence)
            # 去除无用词
            sentence = CleanDataUtil.remove_useless_word(sentence)
            # 去除特殊符号
            sentence = CleanDataUtil.remove_useless_symbol(sentence)
            return sentence
        else:
            return ""

    # 去除网址
    @staticmethod
    def remove_web(string):
        pattern = re.compile(CleanDataUtil.web_reg)
        return pattern.sub(" ", string)

    @staticmethod
    def remove_taobao(string):
        pattern = re.compile(CleanDataUtil.taobao_reg)
        return pattern.sub(" ", string)

    @staticmethod
    def remove_useless_word(string):
        for word in CleanDataUtil.useless_words:
            if (word in string):
                string = string.replace(word, ' ')
        return string

    @staticmethod
    def remove_useless_symbol(string):
        pattern = re.compile(CleanDataUtil.useless_symbol)
        return pattern.sub("", string)
