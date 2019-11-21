from utils import config
from utils.clean_data_util import CleanDataUtil
from pathlib import Path
import pandas as pd
import jieba

# userdict
jieba.load_userdict(config.user_dict)


# 生成userdict
def get_user_dict(train_data_frame, test_data_frame):
    data = []
    data.extend(train_data_frame['Brand'].to_list())
    data.extend(train_data_frame['Model'].to_list())
    data.extend(test_data_frame['Brand'].to_list())
    data.extend(test_data_frame['Model'].to_list())
    user_dict_set = set(data)
    with open(config.user_dict, 'w', encoding="UTF-8") as file:
        for user in user_dict_set:
            if isinstance(user, str):
                file.write(CleanDataUtil.remove_useless_symbol(user) + '\n')


# 去除停用词

def remove_stop_words(words):
    return [word for word in words if word not in stop_words]


# 加载停用词

def load_stop_words():
    file = open(config.stop_word_path, 'r', encoding="UTF-8")
    stop_words = file.readlines()
    stop_words = [stop_word.strip() for stop_word in stop_words]
    return set(stop_words)


# 获取训练集与测试集

def get_data_frame(test_data_path, train_data_path):
    train_data_frame = pd.read_csv(test_data_path, encoding="UTF-8")
    test_data_frame = pd.read_csv(train_data_path, encoding="UTF-8")
    return train_data_frame, test_data_frame


def cut(sentence, is_remove_stop_words=True):
    words = jieba.cut(sentence)
    if is_remove_stop_words:
        words = remove_stop_words(words)
    return words


# 停用词
stop_words = load_stop_words()

if __name__ == '__main__':
    # 生成userdict
    train_data, test_data = get_data_frame(config.train_data_path, config.test_data_path)
    get_user_dict(train_data, test_data)
