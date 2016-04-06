import re

print """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&searchby=F&search={search}&hothigh=G&option=G&x=19&y=2&currpage={currpage}
""".format(search='COMPUTER+SCIENCE', currpage=1)

a = """https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=G&option=G&searchby=F&search=COMPUTER%20SCIENCE&hothigh=G&x=1&y=7&currpage=1"""
b = a[:-1] + str(int(a[-1])+1)
print b



wos_link = """
https://vpn.nuist.edu.cn/gateway/,DanaInfo=.agbvh0f4G4nlzrx13A2ww0zVzA.+Gateway.cgi?&GWVersion=2&SrcAuth=ESI&SrcApp=ESI&DestLinkType=FullRecord&DestApp=WOS&SrcAppSID=P1BtMTHmCHWyEAoYEoW&SrcDesc=RETURN_ALT_TEXT&SrcURL=http%3A//esi.webofknowledge.com/paperpage.cgi%3Foption%3DG%26option%3DG%26searchby%3DF%26search%3DCOMPUTER%2520SCIENCE%26hothigh%3DG%26x%3D1%26y%3D7%26currpage%3D16&KeyUT=000237147400001&SrcImageURL=
"""

print re.search("KeyUT=[\d]*&", wos_link).group()
print re.search("KeyUT=([\d]*)&", wos_link).group(1)

print 'KeyUT' in wos_link
