"""teleauto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from auto import views as auto_views 

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^tasks/$', auto_views.TaskListCreate.as_view()),
    re_path('^callback/$', auto_views.CallBackView.as_view(), name='callback-url'),
    re_path('^packages/(?:(?P<action>\d+)/)?$', auto_views.PackageList.as_view()),
    re_path('^tele/automate/$', auto_views.TelegramChannelInfoUpdateView.as_view()),
    re_path('^runningtasks/$', auto_views.RunningTaskView.as_view()),
    
    
]
