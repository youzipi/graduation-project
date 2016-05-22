# -*- coding: utf-8 -*-
from pattern.text.en import lemma
from pymongo import MongoClient


# splits = re.compile('[\s\[\]\?().,;:\'"/]+')
# import re
# is_num = re.compile('^[\d|-|=]+$')


class Cleaned(object):
    def __init__(self, host='127.0.0.1:27017', db_name='esi', doc_name='test',
                 ):
        self.host = host
        self.db_name = db_name
        self.doc_name = doc_name

        # self.reset_result = reset_result + datetime.datetime.now().strftime("tmp_%Y-%m-%d_%H%M%S")
        self._conn()

    def _conn(self):
        self.client = MongoClient(self.host)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.doc_name]

    def clean(self, key):
        """
        清洗数据库字段后,放回原document的`cleaned_字段名`中
        :param key: 需要清洗的字段
        :return:
        """
        assert isinstance(key, (str, unicode))

        target_field = 'cleaned_' + key

        docs = self.collection.find()

        for doc in docs:
            word_list = doc[key]
            cleaned_list = self._collect_words_d(word_list)
            self.collection.update_one({'_id': doc.get('_id')},
                                       {"$set": {target_field: cleaned_list}})

    @staticmethod
    def _collect_words_d(word_list):
        cleaned_list = []
        for w in word_list:  # type: str
            # 去除左右空格
            w = w.strip()
            w = lemma(w)
            cleaned_list.append(w)
        return cleaned_list

    def _close_conn(self):
        self.client.close()

    def close_conn(self):
        self._close_conn()


if __name__ == "__main__":
    c = Cleaned(doc_name='test')
    c.clean(key='keywords')
    c.clean(key='research_areas')

# 提取词根后 ,太简化 ,有些原意失去了
"""
stemmer = SnowballStemmer('english')
stemmer.stem(word)

WordNetLemmatizer
"""


def dict2intDict(d):
    """
    因为mongoDB里面的dict以object形式存在(1.key 只能为 字符串 => 2. key 的顺序乱了(还有python的原因))
    ,这里重新构造一个 key 为 int 的 dict
    :param d:
    :return:
    """
    target = {}
    for i in d:
        target.update({int(i): d[i]})
    return target
