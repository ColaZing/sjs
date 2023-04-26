from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from sjsapp.models import SJUser, SJWork, SJTask, SJOrder


# Create your views here.
def cs(request):
    return render(request, 'tasks.html')


@csrf_exempt
def signin(request):
    if request.method == 'GET':
        # 清理session
        request.session.flush()
        return render(request, 'signin.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 判断用户名和密码是否正确
        if SJUser.objects.filter(username=username, password=password):
            # 记录用户登录状态ID到session中
            request.session['uid'] = SJUser.objects.get(username=username).id
            # 登录成功，跳转到任务列表页面
            return HttpResponseRedirect('/index/')
        else:
            # 登录失败，跳转到登录页面
            return render(request, 'signin.html', {'error': '用户名或密码错误'})


@csrf_exempt
def signup(request):
    if request.method == 'GET':
        request.session.flush()
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        area = request.POST.get('area')
        gender = request.POST.get('gender')
        role = '雇主'

        # 判断用户名是否存在
        if SJUser.objects.filter(username=username):
            return render(request, 'signup.html', {'error': '用户名已存在'})
        else:
            SJUser.objects.create(username=username, password=password, email=email, phone=phone, area=area,
                                  gender=gender, role=role)
            # 注册成功，跳转到登录页面
            return HttpResponseRedirect('/signin/')


@csrf_exempt
def design_signup(request):
    if request.method == 'GET':
        request.session.flush()
        return render(request, 'designsignup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        area = request.POST.get('area')
        gender = request.POST.get('gender')
        role = '设计师'
        skill = request.POST.get('skill')
        introduction = request.POST.get('introduction')

        # 判断用户名是否存在
        if SJUser.objects.filter(username=username):
            return render(request, 'designsignup.html', {'error': '用户名已存在'})
        else:
            SJUser.objects.create(username=username, password=password, email=email, phone=phone, area=area,
                                  gender=gender, role=role, skill=skill, introduction=introduction)
            # 注册成功，跳转到登录页面
            return HttpResponseRedirect('/signin/')


@csrf_exempt
def index(request):
    # 获取全部用户role为设计师的用户
    sj = SJUser.objects.filter(role='设计师')
    # 取出session中的uid
    uid = request.session.get('uid')
    if not uid:
        return render(request, 'index.html', {'sj': sj})
    else:
        # 取出对应的用户对象
        user = SJUser.objects.get(id=uid)
        return render(request, 'index.html', {'user': user, 'sj': sj})


@csrf_exempt
def search(request):
    wd = request.POST.get('wd')
    # 查找用户名中包含wd的用户和skill中包含wd的用户
    sj = SJUser.objects.filter(username__contains=wd, role='设计师') | SJUser.objects.filter(skill__contains=wd,
                                                                                             role='设计师')
    uid = request.session.get('uid')
    if not uid:
        return render(request, 'index.html', {'sj': sj})
    else:
        user = SJUser.objects.get(id=uid)
        return render(request, 'index.html', {'user': user, 'sj': sj})


@csrf_exempt
def detail(request):
    uid = request.session.get('uid')
    did = request.GET.get('did')
    # 取出对应的用户对象
    designuser = SJUser.objects.get(id=did)
    # 在作品表中查找work_designer为designuser的作品
    works = SJWork.objects.filter(work_designer=designuser)
    if not uid:
        return render(request, 'detail.html', {'designuser': designuser, 'works': works})
    else:
        user = SJUser.objects.get(id=uid)
        return render(request, 'detail.html', {'user': user, 'designuser': designuser, 'works': works})


@csrf_exempt
def contant(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        did = request.GET.get('did')
        # 取出对应的用户对象
        designuser = SJUser.objects.get(id=did)
        user = SJUser.objects.get(id=uid)
        return render(request, 'contant.html', {'user': user, 'designuser': designuser})
    elif request.method == 'POST':
        uid = request.POST.get('uid')
        did = request.POST.get('did')
        designuser = SJUser.objects.get(id=did)
        user = SJUser.objects.get(id=uid)
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        days = request.POST.get('days')
        money = request.POST.get('money')
        contact = request.POST.get('contact')
        phone = request.POST.get('phone')
        #         创建任务
        SJTask.objects.create(task_name=name, task_desc=desc, task_expect_day=days, task_money=money,
                              task_contact=contact,
                              task_phone=phone, task_receiver=designuser, task_publisher=user, task_status='待处理')
        return HttpResponseRedirect('/index/')


@csrf_exempt
def tasks(request):
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    tasks = SJTask.objects.filter(task_receiver=user, task_status='待处理')
    tid = request.GET.get('tid')
    if tid:
        task = SJTask.objects.get(id=tid)
        task.task_status = '已接受'
        task.task_receiver = user
        print(task.task_receiver)
        task.save()
        SJOrder.objects.create(order_status='进行中', order_amount=task.task_money, order_task=task)
        return HttpResponseRedirect('/index/')
    return render(request, 'tasks.html', {'user': user, 'tasks': tasks})


@csrf_exempt
def alltasks(request):
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    tasks = SJTask.objects.filter(task_status='待处理', task_receiver__isnull=True)
    tid = request.GET.get('tid')
    if tid:
        task = SJTask.objects.get(id=tid)
        task.task_status = '已接受'
        task.task_receiver = user
        print(task.task_receiver)
        task.save()
        # 创建订单
        SJOrder.objects.create(order_status='进行中', order_amount=task.task_money, order_task=task)
        return HttpResponseRedirect('/index/')
    return render(request, 'tasks.html', {'user': user, 'tasks': tasks})


@csrf_exempt
def newtask(request):
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    if request.method == 'GET':
        return render(request, 'newtask.html', {'user': user})
    elif request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        days = request.POST.get('days')
        money = request.POST.get('money')
        contact = request.POST.get('contact')
        phone = request.POST.get('phone')
        SJTask.objects.create(task_name=name, task_desc=desc, task_expect_day=days, task_money=money,
                              task_contact=contact,
                              task_phone=phone, task_publisher=user, task_status='待处理')
        return HttpResponseRedirect('/index/')


@csrf_exempt
def account(request):
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    print(user)
    # 获取用户的所有订单
    orders_fb = SJOrder.objects.filter(order_task__task_publisher=user)
    orders_js = SJOrder.objects.filter(order_task__task_receiver=user)
    # 获取用户发起的所有任务，任务状态是待接单
    tasks_fb = SJTask.objects.filter(task_publisher=user, task_status='待处理')
    # 获取用户的全部作品
    works = SJWork.objects.filter(work_designer=user)
    print(works)
    if request.method == 'GET':
        return render(request, 'account.html',
                      {'user': user, 'orders_fb': orders_fb, 'orders_js': orders_js, 'works': works,
                       'tasks_fb': tasks_fb,'tz':'info'})


@csrf_exempt
def edit(request):
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)

    username = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    area = request.POST.get('area')
    skill = request.POST.get('skill')
    introduction = request.POST.get('introduction')

    if not username:
        username = user.username
    if not email:
        email = user.email
    if not phone:
        phone = user.phone
    if not area:
        area = user.area
    if not skill:
        skill = user.skill
    if not introduction:
        introduction = user.introduction

    user.username = username
    user.email = email
    user.phone = phone
    user.area = area
    user.skill = skill
    user.introduction = introduction
    user.save()
    # 获取用户的所有订单
    orders_fb = SJOrder.objects.filter(order_task__task_publisher=user)
    orders_js = SJOrder.objects.filter(order_task__task_receiver=user)
    # 获取用户发起的所有任务，任务状态是待接单
    tasks_fb = SJTask.objects.filter(task_publisher=user, task_status='待处理')
    # 获取用户的全部作品
    works = SJWork.objects.filter(work_designer=user)
    print(works)

    return render(request, 'account.html',
                  {'user': user, 'orders_fb': orders_fb, 'orders_js': orders_js, 'works': works,
                   'tasks_fb': tasks_fb, 'tz': 'info'})



@csrf_exempt
def order(request):
    print('task')
    oid = request.GET.get('oid')
    statue = request.GET.get('statue')
    order = SJOrder.objects.get(id=oid)
    if statue == '1':
        order.order_status = '已完成'
        order.save()
    elif statue == '2':
        order.order_status = '已交付'
        order.save()
    elif statue == '3':
        order.order_status = '已取消'
        order.save()
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    print(user)
    # 获取用户的所有订单
    orders_fb = SJOrder.objects.filter(order_task__task_publisher=user)
    orders_js = SJOrder.objects.filter(order_task__task_receiver=user)
    # 获取用户发起的所有任务，任务状态是待接单
    tasks_fb = SJTask.objects.filter(task_publisher=user, task_status='待处理')
    # 获取用户的全部作品
    works = SJWork.objects.filter(work_designer=user)
    print(works)

    return render(request, 'account.html',
                  {'user': user, 'orders_fb': orders_fb, 'orders_js': orders_js, 'works': works,
                   'tasks_fb': tasks_fb, 'tz': 'task'})


@csrf_exempt
def delworks(request):
    wid = request.GET.get('wid')
    work = SJWork.objects.get(id=wid)
    work.delete()
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    print(user)
    # 获取用户的所有订单
    orders_fb = SJOrder.objects.filter(order_task__task_publisher=user)
    orders_js = SJOrder.objects.filter(order_task__task_receiver=user)
    # 获取用户发起的所有任务，任务状态是待接单
    tasks_fb = SJTask.objects.filter(task_publisher=user, task_status='待处理')
    # 获取用户的全部作品
    works = SJWork.objects.filter(work_designer=user)
    print(works)

    return render(request, 'account.html',
                  {'user': user, 'orders_fb': orders_fb, 'orders_js': orders_js, 'works': works,
                   'tasks_fb': tasks_fb, 'tz': 'zp'})


@csrf_exempt
def work(request):
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    wid = request.POST.get('wid')
    if wid != 'new':
        edwork = SJWork.objects.get(id=wid)
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        img = request.FILES.get('img')
        price = request.POST.get('price')
        if not price:
            price = edwork.work_price
        if not name:
            name = edwork.work_name
        if not desc:
            desc = edwork.work_desc
        if not img:
            img = edwork.work_img
        edwork.work_name = name
        edwork.work_desc = desc
        edwork.work_img = img
        edwork.work_price = price
        edwork.save()
    else:
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        img = request.FILES.get('img')
        price = request.POST.get('price')
        SJWork.objects.create(work_name=name, work_desc=desc, work_img=img, work_price=price, work_designer=user)

    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    print(user)
    # 获取用户的所有订单
    orders_fb = SJOrder.objects.filter(order_task__task_publisher=user)
    orders_js = SJOrder.objects.filter(order_task__task_receiver=user)
    # 获取用户发起的所有任务，任务状态是待接单
    tasks_fb = SJTask.objects.filter(task_publisher=user, task_status='待处理')
    # 获取用户的全部作品
    works = SJWork.objects.filter(work_designer=user)
    print(works)

    return render(request, 'account.html',
                  {'user': user, 'orders_fb': orders_fb, 'orders_js': orders_js, 'works': works,
                   'tasks_fb': tasks_fb, 'tz': 'zp'})


@csrf_exempt
def edittask(request):
    tid = request.GET.get('tid')
    task = SJTask.objects.get(id=tid)
    task.task_status = '已取消'
    task.save()
    uid = request.session.get('uid')
    user = SJUser.objects.get(id=uid)
    print(user)
    # 获取用户的所有订单
    orders_fb = SJOrder.objects.filter(order_task__task_publisher=user)
    orders_js = SJOrder.objects.filter(order_task__task_receiver=user)
    # 获取用户发起的所有任务，任务状态是待接单
    tasks_fb = SJTask.objects.filter(task_publisher=user, task_status='待处理')
    # 获取用户的全部作品
    works = SJWork.objects.filter(work_designer=user)
    print(works)

    return render(request, 'account.html',
                  {'user': user, 'orders_fb': orders_fb, 'orders_js': orders_js, 'works': works,
                   'tasks_fb': tasks_fb, 'tz': 'task'})


@csrf_exempt
def dash(request):
    if request.method == 'GET':
        # 查询订单总数
        order = SJOrder.objects.all()
        ordernum = len(order)
        # 查询订单总额
        total = 0
        for i in order:
            total += i.order_amount
        # 查询用户总数
        user = SJUser.objects.all()
        usernum = len(user)
        # 获取全部分类

        return render(request, 'dash.html',
                      {'ordernum': ordernum, 'total': total, 'usernum': usernum,
                       'orders': order})
    else:
        StartData = request.POST.get('StartData')
        EndData = request.POST.get('EndData')
        category = request.POST.get('category')
        # 查询起止时间内category的订单总数
        order = SJOrder.objects.filter(order_create_time__range=(StartData, EndData))
        ordernum = len(order)
        # 查询订单总额
        total = 0
        for i in order:
            total += i.order_amount
        # 查询用户总数
        user = SJUser.objects.all()
        usernum = len(user)

        return render(request, 'dash.html',
                      {'ordernum': ordernum, 'total': total, 'usernum': usernum,
                       'orders': order})
