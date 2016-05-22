
# coding: utf-8

# In[7]:

get_ipython().magic(u'matplotlib inline')
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pymongo
sns.set(style="white", context="talk")
# sns.set_style('white')

# from bokeh.plotting import figure,show,output_notebook
from bokeh.charts import Bar, output_notebook, show,Histogram,hplot,Line
from bokeh import plotting
plotting.output_notebook()
output_notebook()


# In[5]:

client = pymongo.MongoClient(host='127.0.0.1', port=27017)

db_name = 'esi'
doc_name = 'test'
db = client[db_name]
papers_collection = db['test']
abstract_rank_collection = db['AR3']


# In[6]:

pipeline = [
{'$unwind':"$authors"},
{'$group':
    {
        '_id':{'_id':'$_id','citations':'$citations','wos_no':'$wos_no'},
        'author_count':{'$sum':1},
        }
},
{'$group':
    {
        '_id':'$author_count',
        'paper_count':{'$sum':1},
        'citations_all':{'$sum':'$_id.citations'},
        'citations_avg':{'$avg':'$_id.citations'}
    }
},
{'$project':
    {
        'author_count':"$_id",
        '_id':0,
        'paper_count':1,
        'citations_avg':1

    }
    
},
{'$sort':{'author_count':1}}
]
pp = pd.DataFrame(list(papers_collection.aggregate(pipeline)))
pp.loc[:,['author_count','paper_count']]
pp.loc[:,['author_count','citations_avg']]


# In[ ]:




# In[ ]:




# 
# ### c1
# 绝大部分论文是在2～5个人内
# ### c2
# 几乎和c1是相反的，
# 个人完成的论文被引用数排在第3，能力极强的个人
# 9，10人合作的被引用数排在第2，1，多机构合作，资源更丰富，发表后，更容易被涉及的机构引用
# 参与人数3，4，5的明显划水更多（主动，被动）
# 

# In[10]:

# p = Histogram(pp.loc[:,['author_count','paper_count']],values='paper_count',label='author_count')
p = Bar(pp)
p1 = Bar(pp, label='author_count', values='paper_count',
        title=u"作者数量－论文数量")
p2 = Bar(pp, label='author_count', values='citations_avg',
        title=u"作者数量-每篇论文被引用数")
# p3 = Bar(pp, label='author_count', values='citations_avg',agg='mean',
#         title=u"作者数量-每篇论文被引用数")
# p4 = Bar(pp, label='author_count', values='citations_avg',agg='avg',
#         title=u"作者数量-每篇论文被引用数") not support allowed values are sum, mean, count, nunique, median, min or max
show(p1)
show(p2)

# show(p3)
# show(p4)


# In[11]:

pipeline = [
{'$unwind': '$cleaned_keywords'}
,{'$match': {
        'pub_year': {'$in':[2013,2014,2015]}
    }
}
, {
    '$group': {
        '_id': {'keywords': '$cleaned_keywords'},
        'paper_count': {'$sum': 1},
    }
}
, {'$sort': {'paper_count': -1}}
,{'$project':{
        '_id':0,
        'keywords':'$_id.keywords',
    }
   }
,{'$limit':30}
]
keyword_30_docs = list(papers_collection.aggregate(pipeline))
keyword_30 = list(i.get('keywords') for i in keyword_30_docs)
print keyword_30 # 关键字列表，[u'system',u'model',...]
# print keyword_30_docs


# In[70]:


pipeline = [
{'$unwind': '$cleaned_keywords'}
, {'$match': {
        'cleaned_keywords': {'$in':keyword_30}
    }
}
,{'$group': {
        '_id': {'keywords': '$cleaned_keywords','pub_year':'$pub_year'},
        'paper_count': {'$sum': 1},
    }
}
,{'$project':{
    'keywords':'$_id.keywords',
    'paper_count':1,
    'pub_year':'$_id.pub_year',
    '_id':0
        }
 }
,{
    '$group': {
        '_id': {'keywords': '$keywords'},
        'year_citations':{'$addToSet':'$$ROOT'}
    }
}
]
keyword_30_yearly = list(papers_collection.aggregate(pipeline))
# print(keyword_30_yearly)
cleaned_k_30 = list(i.get('_id').get('keywords') for i in keyword_30_yearly)
# print(keyword_30_yearly[0])
# print(cleaned_k_30)  # 关键字列表，[u'system',u'model',...]
year_citations = list(i.get('year_citations') for i in keyword_30_yearly)
# yc0 = year_citations[0]
print year_citations[0][0].get('pub_year')
print year_citations[0][0].get('paper_count')
data = []# result
for yc in year_citations:
    d = {}
    for i in yc:
        year = int(i.get('pub_year'))
        paper_count = i.get('paper_count')
        d.update({year:paper_count})
#     print d
    item = {}
    item['keywords'] = yc[0].get('keywords')
    item['year_citations'] = d
    data.append(item)

print data
# for data in year_citations:
#     print data


# In[78]:

xyvalues = np.array([[2, 3, 7, 5, 26], [12, 33, 47, 15, 126], [22, 43, 10, 25, 26]])

line = Line(data=xyvalues, x=['2012','2013','2014','2015','2016'],title="line", legend="top_left", ylabel='Languages')

show(line)


# In[85]:

from bokeh.plotting import figure, output_notebook, show
output_notebook()
p = figure(plot_width=400, plot_height=400)

# add a line renderer
p.line([2012, 2013, 2014, 2015, 2016], [[6, 7, 2, 4, 5],[7, 2, 4, 6, 5]], line_width=2)

show(p)


# In[103]:

# colors_list = ['blue', 'yellow']
legends_list = ['first', 'second']
xs= [[1,2,3] for i in range(10)]
ys=[[6, 5, 2], [4, 5, 7]]
p = figure(plot_width=300, plot_height=300)
for (leg, x, y ) in zip(legends_list, xs, ys):
    print 1
    my_plot = p.line(x, y,legend= leg)

show(p)


# In[92]:

from bokeh.plotting import figure, output_notebook, show

p = figure(plot_width=300, plot_height=300,x_range=['2012','2013','2014'])
p.multi_line(
#     xs=[[1, 2, 3], [1, 3, 4]], 
    ys=[[6, 7, 2], [4, 5, 7]],
             color=['red','green'])

show(p)


# In[75]:

f,(ax1,ax2) = plt.subplots(2,1,sharex=True)
sns.barplot(x=pp['author_count'],y=pp['paper_count'],palette='Set3',ax=ax1)
sns.barplot(x=pp['author_count'],y=pp['citations_avg'],palette='Set3',ax=ax2)


# In[41]:

x = np.random.randn(100)
x


# In[74]:

import numpy as np

# (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
# data = dict(
#     python=[2, 3, 7, 5, 26, 221, 44, 233, 254, 265, 266, 267, 120, 111],
#     pypy=[1:12, 2:33, 3:47, 4:15, 5:126, 6:121, 7:144, 233, 254, 225, 226, 267, 110, 130],
#     'pypy'=[
#         2005=12,
#         2006:11,
#         2007:17
# #     ]
#     jython=[22, 43, 10, 25, 26, 101, 114, 203, 194, 215, 201, 227, 139, 160],
# )
# data = {kk=2: 12, 3: 14}}
p = figure()
line = p.line(x=[1,2,3,4,5],y=[5,4,3,2,1])

show(line)


# In[40]:

ax = sns.distplot(x)


# In[20]:

docs_all = abstract_rank_collection.find()
docs_count = abstract_rank_collection.find().count()
count_all = 0
for i in docs_all:
    count_all += i['count']
print count_all
print docs_count
print count_all/docs_count
docs_count_20 = docs_count*0.2
print docs_count_20


# In[11]:

papers = papers_collection.find(projection=['citations','authors']).sort('citations',pymongo.DESCENDING).limit(10)
papers


# In[12]:

for i in papers:
    print i


# In[13]:

top_count = abstract_rank_collection.find().sort('count', pymongo.DESCENDING).limit(1)[0]['count']
print top_count


# In[15]:

series = pd.Series(3 * np.random.rand(4), index=['a', 'b', 'c', 'd'], name='count')
# series.plot.pie(figsize=(6, 6))
series.plot.pie(labels=['AA', 'BB', 'CC', 'DD'],autopct='%.2f', fontsize=20, figsize=(6, 6))


# In[16]:

docs_20 = abstract_rank_collection.find().sort('count', pymongo.DESCENDING).limit(20)
docs_20_percent = abstract_rank_collection.find().sort('count', pymongo.DESCENDING).limit(int(docs_count_20))

count_20 = 0
for i in docs_20_percent:
    count_20 += i['count']
print count_20
print count_20/float(count_all)


# In[17]:

abstract_rank = pd.DataFrame(list(docs))


# In[36]:

abstract_rank


# In[2]:

g = sns.factorplot(x="_id", y="count", data=abstract_rank,
                   size=20, kind="bar", palette="muted")


# In[ ]:



