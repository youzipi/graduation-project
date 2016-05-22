
# coding: utf-8

# In[139]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[161]:

tables = pd.read_excel(u'./datas/中奖名单.xlsx')


# In[162]:

column_names = tables.columns


# In[163]:

len(tables)


# In[164]:

tables.columns


# In[165]:

tables.shape


# In[166]:

column = tables[u'签收'+'.5']


# In[167]:

type(column)
column.reindex


# In[169]:

tables[tables[u'签收'].str().contaions('OF') == True]


# In[175]:

tables[tables[u'签收.5'].str.contains('OF') > 0]


# In[100]:

column.str.contains('OF').str.len()

