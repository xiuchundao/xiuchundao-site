### 介绍

使用Flask开发的博客，地址是[xiuchundao.me](http://xiuchundao.me)。虽然问题还很多，但是现在凑合着暂时能用，后期慢慢完善，有需要的同学自己fork。一定要阅读下面的`注意部分`!

### 开发

先确保python>=2.6，pip、virtualenv都安装

```
	$ git clone your_fork
	$ cd xiuchundao-site
	$ rm -rf migrations
	$ virtualenv --distribute venv
	$ source venv/bin/activate
	(venv)$ pip install -r requirements.txt
	(venv)$ python manage.py create_db
	(venv)$ python manage.py runserver --host 0.0.0.0 --port 5000
```

### 注意

1. clone之后，将根目录下manage.py文件中的`create_app(‘product’)`改为`create_app(‘development’)`，这样会使用本地sqlite数据库
2. clone之后，将根目录下的migrations文件夹删除，这个是我正式数据库的迁移脚本，对你没用。否则执行`python manage.py create_db`会出现问题
3. 手动部署教程可参照[博客部署过程记录](https://xiuchundao.me/post/records-of-deploying)，同时注意app->web->template->_base.html中关于Google Analytics的代码对你也没用