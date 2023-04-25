from django.db import models


# Create your models here.
# 用户表
class SJUser(models.Model):
    gender_choice = (
        ('男', '男'),
        ('女', '女'),
    )
    role_choice = (
        ('雇主', '雇主'),
        ('设计师', '设计师'),
    )
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=11, verbose_name='手机号')
    area = models.CharField(max_length=20, verbose_name='地区')
    # 性别
    gender = models.CharField(choices=gender_choice, max_length=10, verbose_name='性别')
    # 角色
    role = models.CharField(choices=role_choice, max_length=10, verbose_name='角色')
    # 技能
    skill = models.CharField(max_length=255, verbose_name='技能', default='雇主无技能')
    # 个人简介
    introduction = models.CharField(max_length=255, verbose_name='个人简介', default='雇主无简介')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户管理'


# 任务表
class SJTask(models.Model):
    task_status_choice = (
        ('待处理', '待处理'),
        ('已接受', '已接受'),
        ('已取消', '已取消'),
    )
    # 任务名称
    task_name = models.CharField(max_length=20, verbose_name='任务名称')
    # 任务描述
    task_desc = models.CharField(max_length=255, verbose_name='任务描述')
    # 任务状态
    task_status = models.CharField(choices=task_status_choice, max_length=20, verbose_name='任务状态')
    # 任务发布者
    task_publisher = models.ForeignKey(SJUser, on_delete=models.CASCADE, verbose_name='任务发布者')
    # 任务接受者
    task_receiver = models.ForeignKey(SJUser, on_delete=models.CASCADE, verbose_name='任务接受者')
    # 任务创建时间
    task_create_time = models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')

    class Meta:
        verbose_name = '任务管理'


# 订单表
class SJOrder(models.Model):
    order_status_choice = (
        ('进行中', '进行中'),
        ('已交付', '已交付'),
        ('已完成', '已完成'),
        ('已取消', '已取消'),
    )
    # 订单状态
    order_status = models.CharField(choices=order_status_choice, max_length=20, verbose_name='订单状态')
    # 订单创建时间
    order_create_time = models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')
    # 订单金额
    order_amount = models.FloatField(verbose_name='订单金额')
    # 订单所属任务
    order_task = models.ForeignKey(SJTask, on_delete=models.CASCADE, verbose_name='订单所属任务')

    class Meta:
        verbose_name = '订单管理'


# 作品表
class SJWork(models.Model):
    # 设计师
    work_designer = models.ForeignKey(SJUser, on_delete=models.CASCADE, verbose_name='设计师')
    # 作品名称
    work_name = models.CharField(max_length=20, verbose_name='作品名称')
    # 作品描述
    work_desc = models.CharField(max_length=255, verbose_name='作品描述')
    # 作品创建时间
    work_create_time = models.DateTimeField(auto_now_add=True, verbose_name='作品创建时间')
    # 作品图片
    work_img = models.ImageField(upload_to='work_img', verbose_name='作品图片')
    # 案例要价
    work_price = models.FloatField(verbose_name='案例要价')

    class Meta:
        verbose_name = '作品管理'
