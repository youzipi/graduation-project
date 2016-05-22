
# coding: utf-8

# In[2]:

from bokeh.sampledata.autompg import autompg as df
from bokeh.charts import Histogram, output_notebook, show, hplot
# print df
output_notebook()


# In[16]:

hist = Histogram(df, values='mpg', title="Auto MPG Histogram", width=400)
hist2 = Histogram(df, values='displ', label='cyl', color='cyl', legend='top_right',
                  title="MPG Histogram by Cylinder Count", width=400)

show(hplot(hist, hist2))


# In[5]:

# Modules needed from Bokeh.
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d

# Seting the params for the first figure.
s1 = figure(x_axis_type="datetime",plot_width=1000,
           plot_height=600)

# Setting the second y axis range name and range
s1.extra_y_ranges = {"foo": Range1d(start=-100, end=200)}

# Adding the second axis to the plot.  
s1.add_layout(LinearAxis(y_range_name="foo"), 'right')

# Setting the rect glyph params for the first graph. 
# Using the default y range and y axis here.           
s1.rect(df_j.timestamp, mids, w, spans, fill_color="#D5E1DD", line_color="black")

# Setting the rect glyph params for the second graph. 
# Using the aditional y range named "foo" and "right" y axis here. 
s1.rect(df_j.timestamp, ad_bar_coord, w, bar_span,
         fill_color="#D5E1DD", color="green", y_range_name="foo")

# Show the combined graphs with twin y axes.
show(s1)


# In[ ]:




# In[ ]:



