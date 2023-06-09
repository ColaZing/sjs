"""sjs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from sjsapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('search/', views.search),
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('designsignup/', views.design_signup),
    path('detail/', views.detail),
    path('contant/', views.contant),
    path('tasks/', views.tasks),
    path('alltasks/', views.alltasks),
    path('newtask/', views.newtask),
    path('account/', views.account),
    path('edit/', views.edit),
    path('order/', views.order),
    path('delworks/', views.delworks),
    path('editworks/', views.work),
    path('edittask/', views.edittask),
    path('dash/', views.dash),

]
