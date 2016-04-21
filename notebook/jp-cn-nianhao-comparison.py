
# coding: utf-8

# wikipedia:
# 
# https://zh.wikipedia.org/wiki/日本年號列表
# 
# 645~1989
# 
# 明治（1868）之后，“一世一元”，谥号即年号，在世称为“今上天皇”
# 
# https://zh.wikipedia.org/wiki/中国年号列表
# 
# BD140～1949
# 
# ```js
# a = $('#mw-content-text > table> tbody > tr > td:nth-child(2) > a');
# 
# a = $('#mw-content-text > table> tbody > tr > td:nth-child(1) > a');
# 
# for (i in a){console.log(a[i].innerText)};
# ```
# 浏览器控制台，save as... [xxx.log]

# - 出现率前20% 的使用率
# - 两边都特别常用的
# - 日本特别常用，而中国不是太常用的

# In[69]:



import pandas as pd
import numpy as np


# In[251]:

def render(path):
    with open(path,'r') as file:
        datas = file.readlines()
    str_list = []
    length = len(datas)
    for i in xrange(length):
        b = unicode(datas[i].replace('\n',''), "utf-8")
        for j in b:
            str_list += j
    df = pd.DataFrame(data=str_list,columns=['nianhao'])
    return df


# In[252]:

jp_df = render('./japan-nianhao.log')


# In[199]:

a = unicode(jp_datas[0],"utf-8")


# In[200]:

a
print a


# In[201]:

for i in a:
    print i


# In[103]:

a = u'中国'


# In[106]:

a


# In[107]:

type(a)


# In[102]:

print a


# In[307]:

jp_df[u'nianhao'].value_counts()


# In[243]:

jp_counts = len(jp_df[u'nianhao'].values) # 一共使用了506个字次
jp_counts


# In[245]:

jp_words = len(np.unique(jp_df[u'nianhao'].values)) # 一共使用了72个不同的字
jp_words


# In[246]:

jp_counts/float(jp_words)


# In[253]:

cn_df = render('./china-nianhao.log')


# In[308]:

cn_df[u'nianhao'].value_counts()[:20]


# In[255]:

cn_counts = len(cn_df[u'nianhao'].values) 
cn_counts


# In[258]:

cn_words = len(np.unique(cn_df[u'nianhao'].values)) 
cn_words


# In[270]:

cn_counts/float(cn_words)


# In[276]:

cn_unique_words = pd.DataFrame(data=np.unique(cn_df[u'nianhao'].values),columns=['nianhao'])


# In[277]:

jp_unique_words = pd.DataFrame(data=np.unique(jp_df[u'nianhao'].values),columns=['nianhao'])


# In[291]:

jp_index = pd.Index(jp_unique_words)
print jp_index
cn_index = pd.Index(cn_unique_words)
print cn_index


# In[302]:

both = cn_index.intersection(jp_index)
print both
print both.size  # 59


# In[305]:

jp_only = jp_index.difference(cn_index)
print jp_only
print jp_only.size  # 13个，只在日本年号中出现过的词


# In[ ]:



