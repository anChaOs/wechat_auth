微信授权登录demo代码
======================

:Date: 15/01 2017


环境搭建
-----------

.. code:: bash
    
    sudo apt-get install python3.4
    sudo apt-get install python3-pip

    sudo pip3 install -r requirements.txt

    cd wechat_auth
    python3 manager.py shell
    >> from app import db
    >> db.create_all()

运行
--------------------

.. code:: bash
    
    cd wechat_auth
    python3 manager.py runserver
    # Or run in shell
    cd wechat_auth
    python3 manager.py shell


运行
--------------------

    在wechat_auth/config/config.py文件中修改相关的APPID等信息