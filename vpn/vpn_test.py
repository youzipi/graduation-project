import requests

cookies = {

    "DSFirstAccess": "1453365010",
    "DSID": "8b38628dc581689e0b15aad0cd49c357",
    "DSLastAccess": "1453365298",
    "DSSignInURL": "/",
}

"""
https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+paperpage.cgi?option=E&searchby=N&hothigh=G&searchtitle=HTTP&searchscientist=&searchinst=&searchcountry=&searchjournal=&x=30&y=6
"""

r = requests.get('https://vpn.nuist.edu.cn/dana-na/auth/url_default/welcome.cgi',
                 auth=('20121344018', '250036'))

esi = requests.get(
        'https://vpn.nuist.edu.cn/,DanaInfo=.aetkC0jhvntxz8ysswvRv87+highimpacthotpapersmenu.cgi?option=G',
        cookies=cookies,
        # auth=('20121344018', '250036'),
)

print esi.content
