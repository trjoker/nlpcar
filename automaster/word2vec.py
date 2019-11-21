import gensim
from gensim.models.word2vec import LineSentence
from gensim.models import word2vec
# 引入日志配置
import logging

from utils import config

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_model(path):
    model = word2vec.Word2Vec(LineSentence(path), size=200, min_count=5)
    model.save(config.word2vec_model_path)


if __name__ == '__main__':
    # get_model(config.merged_seg_path)
    model = word2vec.Word2Vec.load(config.word2vec_model_path)
    print(model.wv.most_similar(['凯迪拉克'], topn=10))
    # print(model.wv.get_vector("排量"))