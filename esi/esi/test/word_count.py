# -*- coding: utf-8 -*-
import datetime
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import lemma
from pymongo import MongoClient
import collections
import re

# stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()

sw = list(stopwords.words('english'))


# other_words = ['used','propose','provide','show','set','also']
# sw.extend(other_words)


class Count(object):
    def __init__(self, host='127.0.0.1:27017', db_name='esi', doc_name='test',
                 key=None, result=None,
                 show_result=True,
                 reset_result=True,
                 is_arr=False,
                 ):
        self.host = host
        self.db_name = db_name
        self.doc_name = doc_name

        assert isinstance(key, (str, unicode))
        assert isinstance(result, (str, unicode))

        self.key = key
        self.result = result
        self.show_result = show_result
        self.reset_result = reset_result
        # self.reset_result = reset_result + datetime.datetime.now().strftime("tmp_%Y-%m-%d_%H%M%S")

        self.is_arr = is_arr

        self.rank_list = collections.defaultdict(int)
        # todo 用numpy的容器替代

    def _conn(self):
        self.client = MongoClient(self.host)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.doc_name]

    def count(self):
        self._conn()

        docs = self.collection.find()

        if self.is_arr:
            for doc in docs:
                word_list = doc[self.key]
                self._collect_words_d(word_list)
        else:
            for doc in docs:
                words = doc[self.key]
                assert isinstance(words, (str, unicode))
                # split
                word_list = re.split('[\s\[\]\?().,;:\'"/]+', words)
                self._collect_words(word_list)

        self._save_docs()

    def _collect_words_d(self, word_list):
        for w in word_list:  # type: str
            # 去除左右空格
            w = w.strip()
            self.rank_list[w] += 1

    def _collect_words(self, word_list):
        for w in word_list:
            # split 产生了空白字符
            w_len = len(w)
            if w_len == 0:
                continue
            # 有些关键字不能 改成小写 如 C,R,直接保存,因为lemma 会 把所有单词lower
            # if w_len == 1:
            #     rank_list[w] += 1
            # 先小写,为了在stop_words 中筛掉
            if w_len > 1:
                w = w.lower()
            # remove stopwords
            if w in sw:
                continue

            else:
                # 4 stem
                # w = stemmer.stem(w)
                # w = lemmatizer.lemmatize(w)
                # w = singularize(w)
                w = lemma(w)
                self.rank_list[w] += 1

    def _save_docs(self):
        print len(self.rank_list)

        # ex:{'_id':'data','count':2355}
        g = ({'_id': i, 'count': self.rank_list[i]} for i in self.rank_list)

        self.target_collection = self.db[self.result]

        # drop old result_db
        if self.reset_result:
            self.target_collection.drop()

        # insert into mongoDB
        self.target_collection.insert_many(i for i in g)

        if self.show_result:
            for doc in self.target_collection.find().sort('count', -1).limit(20):
                print doc

        self._close_conn()

    def _close_conn(self):
        self.client.close()


if __name__ == "__main__":
    c = Count(key='abstract', result='AR3')
    c.count()

    c = Count(key='research_areas', result='area_rank', is_arr=True)
    c.count()

    c = Count(key='keywords', result='keyword_rank', is_arr=True)
    c.count()

"""The metafor package provides functions for conducting meta-analyses in R. The package includes functions for fitting the meta-analytic fixed- and random-effects models and allows for the inclusion of moderators variables (study-level covariates) in these models. Meta-regression analyses with continuous and categorical moderators can be conducted in this way. Functions for the Mantel-Haenszel and Peto's one-step method for meta-analyses of 2 x 2 table data are also available. Finally, the package provides various plot functions (for example, for forest, funnel, and radial plots) and functions for assessing the model fit, for obtaining case diagnostics, and for tests of publication bias."""

"""
        空白符
        [
        ]
        ,
        .
        (
        )
        "
        """

# 提取词根后 ,太简化 ,有些原意失去了
"""
stemmer = SnowballStemmer('english')
stemmer.stem(word)

WordNetLemmatizer
"""
