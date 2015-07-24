下载安装django, python setup.py install
...
1. runserver.bat, 启动django服务器

2. 打开浏览器, 打开127.0.0.1:8000    log账单监测系统主页

3. 第一次点击同步今日log按钮, 之后自动刷新,不要再点击此按钮, 

4. 通过登录账户按钮选择登录

5. config.ini记录账户用户名和密码

6. 按钮保存已查log 将当前数据记录在new_log文件夹下

7. logAuditing\log_main\view.py 以及其他ticketCheck.py, logRefresh.py文件 负责后端逻辑处理, logAuditing\log_main\templates\index.html 生成网页模板, urls.py 模板内网址和后端函数对应,参见django文档和教程

8. log相对文件目录保存在 config.ini 中！

9. 注意, Sbo ip异常登录时候需要上网站输入安全码,之后不再需要

10. Zhibo nickname和username对应list预先保存在zhibo_dict.ini中！

未完全解决Bug:
1. log文件依旧存在Bug, Waring 收入后没有加冒号":",如果更正此Bug务必在log_main\log_refresh.py中更正相应regex

2. Zhibo 查询用户不存在或者多次查询往日账单输赢记录, session会掉,必须重新登陆！ 比如当日log中有两个Zhibo 代理账号, 查询用户失败后,需要切换登陆,否则无法正确查询zhibo其他账单

3. 组号只对成对投注的log记录生效,如果三个网站为一组需要修改,不影响查询。