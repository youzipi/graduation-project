from selenium import webdriver

login_url = "https://vpn.nuist.edu.cn/dana/home/index.cgi"

sel = webdriver.Chrome()
sel.get(login_url)

try:
    sel.find_element_by_xpath('//*[@id="username_5"]').send_keys('20121344018')
    print 'user success!'
except:
    print 'user error!'
    # time.sleep(1)
# sign in the pasword
try:
    sel.find_element_by_xpath('//*[@id="password_5"]').send_keys('yourPW')
    print 'pw success!'
except:
    print 'pw error!'
    # time.sleep(1)
# click to login
try:
    sel.find_element_by_xpath('//*[@id="btnSubmit_6"]').click()
    print 'click success!'
except:
    print 'click error!'
    # time.sleep(3)
