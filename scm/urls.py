"""scm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Codemanagement.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
    url(r'^RefreshGitdata', RefreshGitdata),
    url(r'^get_all_gitdata', get_all_gitdata),
    url(r'^search_week', Search_week),
    url(r'^search_month', Search_month),
    url(r'^search_year', Search_year),
    url(r'^get_get', get),
    url(r'^Pre_Seven', Pre_Seven),
    url(r'^get_gitlab', get_gitlab),
    url(r'^TotalProject', TotalProject),
    url(r'^gitlab_project/(?P<pk>[0-9]+)/$',SearchProject),
]
