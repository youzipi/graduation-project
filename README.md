#graduation-project


https://trello.com/c/kSkYGOFf/15--

# hash算法

#登录ESI

- vpn登录
- 其他学校路径登录
后期可能失效，需要演示


轮询，线程池 不做了，就用scrapy的


查看网站的 robots.txt
http://www.douban.com/robots.txt

176 页
- init
 'request_depth_max': 176,
 'start_time': datetime.datetime(2016, 4, 6, 15, 35, 3, 18379)}
 'finish_time': datetime.datetime(2016, 4, 6, 15, 43, 59, 363912),
 
并发:
 'request_depth_max': 1,
  'start_time': datetime.datetime(2016, 4, 6, 17, 30, 8, 670742)}
 'finish_time': datetime.datetime(2016, 4, 6, 17, 31, 9, 302380),
 
 
 Number of Citations (by year):
 
 ## xpath 效率
 
- [ ]第一次登陆 需要`建立新会话`

- [ ] wos页面 每篇论文展示的信息没有,没有该信息的话,不显示html标签,而不是置空,所以不能通过`.FR_field[i]` 的选择器去获取信息.


100多行后,报错,访问wos_page 得不到信息
此时的url:
```
https://vpn.nuist.edu.cn/,DanaInfo=.aaqrvD1kiwouy09zttxwSw98+InboundService.do?
UT=WOS%3A000228104300004
&IsProductCode=Yes
&mode=FullRecord
&SID=T17K1ywakGS9LyuV8VM
&product=WOS
&returnLink=http%3A%2F%2Fesi.webofknowledge.com%2Fpaperpage.cgi
%3Foption%3DG%26option%3DG%26searchby%3DF%26search%3DCOMPUTER%2520SCIENCE%26hothigh%3DG%26x%3D19%26y%3D2%26currpage%3D18

&srcDesc=RET2ESI
&SrcApp=CR
&DestFail=http%3A%2F%2Fwww.webofknowledge.com
&Init=Yes
&action=retrieve
&Func=Frame
&customersID=ESI
```

正常的url:

```
https://vpn.nuist.edu.cn/gateway/,DanaInfo=.agbvh0f4G4nlzrx13A2ww0zVzA.+Gateway.cgi?
&GWVersion=2
&SrcAuth=ESI
&SrcApp=ESI
&DestLinkType=FullRecord
&DestApp=WOS
&SrcAppSID=Y22fjklWYETPlbyfUqm
&SrcDesc=RETURN_ALT_TEXT
&SrcURL=http%3A//esi.webofknowledge.com/paperpage.cgi
%3Foption%3DG%26option%3DG%26searchby%3DF%26search%3DCOMPUTER%2520SCIENCE%26hothigh%3DG%26x%3D19%26y%3D2%26currpage%3D44

&KeyUT=000264632300012
&SrcImageURL=
```

wos_no:
- 000311016400008

## python dict Ordereddict