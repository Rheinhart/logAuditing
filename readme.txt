下载安装django, python setup.py install
...
1. runserver.bat, 启动django服务器

2. 打开浏览器, 打开127.0.0.1:8000    log账单监测系统主页

3. 第一次点击同步今日log按钮, 之后自动刷新,不要再点击此按钮

4. config.ini记录账户用户名和密码

5. 按钮保存已查log 将当前数据记录在new_log文件夹下

6. logAuditing\log_main\view.py 以及其他ticketCheck.py, logRefresh.py文件 负责后端逻辑处理, logAuditing\log_main\templates\index.html 生成网页模板, urls.py 模板内网址和后端函数对应,参见django文档和教程