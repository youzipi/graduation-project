```
easy_install lxml
安装vs4python27
install scrapy
pip install bs4
```
H: Help
Ctrl-Shift-P: open the command palette


http://www.linuxforums.org/forum/programming-scripting/119516-solved-difference-bw-ctrl-c-ctrl-d-ctrl-z.html

Ctrl + C To terminate
Ctrl + D signals EOF
Ctrl + Z suppends a program
# pip usage
http://lesliezhu.github.io/public/2014-11-08-pip.html

```
yum install zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

yum -y update

sudo yum -y install epel-release
sudo yum -y install python-pip

# lxml depend on
yum install libxslt-devel

pip install scrapy
pip install -U pip

yum install libffi-devel

yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel

yum install mongodb

```

CentOS7 系统 CentOS-Extras 库中已带 Docker，可以直接安装：

$ sudo yum install docker
安装之后启动 Docker 服务，并让它随系统启动自动加载。

$ sudo service docker start
$ sudo chkconfig docker on

# install Nginx
```
yum install nginx
```

# enhancements
```
 yum install tree
```



https://gist.github.com/clasense4/22007c4cc7ba2b625717


```shell
yum install python-pip -y
yum install python-devel -y
yum install gcc gcc-devel -y
yum install libxml2 libxml2-devel -y
yum install libxslt libxslt-devel -y
yum install openssl openssl-devel -y
yum install libffi libffi-devel -y
CFLAGS="-O0"  pip install lxml
pip install Scrapy==0.16.0
scrapy --version
```


刚装时 没有仔细看 装的32位的python 写的过程中 又装了64的pywin32
http://bbs.csdn.net/topics/391076517