表达式	描述
nodename	选取此节点的所有子节点。
/	从根节点选取。
//	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
.	选取当前节点。
..	选取当前节点的父节点。
@	选取属性。




> 
# xpath
section：
/html/body/table[4]/tbody/tr[3]/td/table[2]

## xpath img src  
http://stackoverflow.com/questions/5738972/how-to-find-an-image-tag-by-filename-using-xpath

```python
//img[contains(@src, 'my_image.png')]
```
# css
body > div.EPAMdiv.main-container > div.NEWfullRecord > form