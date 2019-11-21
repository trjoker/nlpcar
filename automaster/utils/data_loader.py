import pandas as pd
import re
import jieba
from utils import config
from utils.clean_data_util import CleanDataUtil
from utils.cut_util import cut
from utils.multi_proc_utils import parallelize


# 处理dataframe
def data_frame_proc(df):
    for col_name in ['Brand', 'Model', 'Question', 'Dialogue']:
        df[col_name] = df[col_name].apply(sentence_proc)
    if 'Report' in df.columns:
        df['Report'] = df['Report'].apply(sentence_proc)
    return df


# 处理句子
def sentence_proc(sentence):
    # 清理
    sentence = CleanDataUtil.clean_sentence(sentence)
    # 切词
    words = cut(sentence, True)
    return " ".join(words)


# 获取训练集与测试集
def get_data_frame(test_data_path, train_data_path):
    print(config.train_data_path)
    train_data_frame = pd.read_csv(test_data_path, encoding="UTF-8")
    test_data_frame = pd.read_csv(train_data_path, encoding="UTF-8")
    return train_data_frame, test_data_frame


# 生成所需的words
def get_data():
    # 加载数据
    print('加载数据')
    train_data, test_data = get_data_frame(config.train_data_path, config.test_data_path)

    # 去除空数据
    print('去除空数据')
    train_data.dropna(subset=['Question', 'Dialogue', 'Report'], how='any', inplace=True)
    test_data.dropna(subset=['Question', 'Dialogue'], how='any', inplace=True)

    # 清理，切词
    print('清理，切词')
    train_data = parallelize(train_data, data_frame_proc)
    test_data = parallelize(test_data, data_frame_proc)

    # 保存
    print('保存')
    train_data.to_csv(config.train_seg_path, index=None, header=True)
    test_data.to_csv(config.test_seg_path, index=None, header=True)

    # 拼接
    print('拼接')
    train_data['merged'] = train_data[['Question', 'Dialogue', 'Report']].apply(
        lambda x: ' '.join(x),
        axis=1)
    test_data['merged'] = test_data[['Question', 'Dialogue']].apply(lambda x: ' '.join(x),
                                                                    axis=1)
    merged_df = pd.concat([train_data[['merged']], test_data[['merged']]])
    merged_df.to_csv(config.merged_seg_path, index=None, header=False)
    return train_data, test_data, merged_df


# 获取全量词表
def get_vocab():
    merged_df = pd.read_csv(config.merged_seg_path, encoding="UTF-8", header=None)
    words = []
    for sentence in merged_df[0]:
        words += sentence.split(' ')
    vocab = set(words)
    # vocab = {word: index for index, word in enumerate(vocab)}
    with open(config.voceb_path, 'w+', encoding='UTF-8') as f:
        for item in vocab:
            if item:
                f.write(str(item) + '\n')


if __name__ == '__main__':
    # train_data, test_data = get_data_frame(config.train_data_path, config.test_data_path)
    # get_data()
    get_vocab()
