# %matplotlib inline
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pymongo

sns.set(style="white", context="talk")
# sns.set_style('white')

# from bokeh.plotting import figure,show,output_notebook
from bokeh.charts import Bar, output_notebook, show, Histogram,output_file

client = pymongo.MongoClient(host='127.0.0.1', port=27017)

db_name = 'esi'
doc_name = 'test'
db = client[db_name]
papers_collection = db['test']
abstract_rank_collection = db['AR3']
pipeline = [
    {'$unwind': "$authors"},
    {'$group':
        {
            '_id': {'_id': '$_id', 'citations': '$citations', 'wos_no': '$wos_no'},
            'author_count': {'$sum': 1},
        }
    },
    {'$group':
        {
            '_id': '$author_count',
            'paper_count': {'$sum': 1},
            'citations_all': {'$sum': '$_id.citations'},
            'citations_avg': {'$avg': '$_id.citations'}
        }
    },
    {'$project':
        {
            'author_count': "$_id",
            '_id': 0,
            'paper_count': 1,
            'citations_avg': 1

        }

    },
    {'$sort': {'author_count': 1}}
]
pp = pd.DataFrame(list(papers_collection.aggregate(pipeline)))
output_file('1.html')
p = Histogram(pp, values='paper_count', label='author_count', color='author_count', bins=None)
show(p)
