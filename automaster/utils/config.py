# -*- coding:utf-8 -*-
# Created by LuoJie at 11/16/19
import os
import pathlib

# 获取项目根目录
root = pathlib.Path(os.path.abspath(__file__)).parent.parent

# 训练数据路径
train_data_path = os.path.join(root, 'datas', 'AutoMaster_TrainSet.csv')
# 测试数据路径
test_data_path = os.path.join(root, 'datas', 'AutoMaster_TestSet.csv')
# 停用词路径
stop_word_path = os.path.join(root, 'datas', 'stopwords/哈工大停用词表.txt')

# 自定义切词表
user_dict = os.path.join(root, 'datas', 'user_dict.txt')

# 预处理后的训练数据
train_seg_path = os.path.join(root, 'datas', 'train_seg_data.csv')
# 预处理后的测试数据
test_seg_path = os.path.join(root, 'datas', 'test_seg_data.csv')
# 合并训练集测试集数据
merged_seg_path = os.path.join(root, 'datas', 'merged_train_test_seg_data.csv')
# 词汇:index 对应表
voceb_path = os.path.join(root, 'datas', 'vocebs.txt')
# 模型路径
word2vec_model_path = os.path.join(root, 'datas', 'word2vec.model')
