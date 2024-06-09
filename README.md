# DjangoProject
 Django实现后台管理系统，含Echarts图表绘制，自定义分页组件，用户认证中间件
# 有关数据库链接问题
1>修改对应settting.py下数据库名字，用户名，密码
<p>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gx_day16',  # 数据库名字
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',  # 那台机器安装了MySQL
        'PORT': 3306,
    }
}
</p>
2>ctrl+alt+r打开终端,输入数据库迁移命令
1.makemigrations
2.migrate 来应用迁移到数据库