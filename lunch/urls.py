"""LunchPoll URL Configuration

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
from . import views

app_name = 'lunch'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tab/(?P<tab>[0-9])/$', views.index, name='index_arg'),
    url(r'^post/create/$', views.create_post, name='create_post'),

    url(r'^post/(?P<slug>[\w-]+)/$', views.detail_post, name='detail_post'),
    url(r'^post/(?P<slug>[\w-]+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', views.edit_post, name='edit_post'),


    url(r'^restaurant/add/$', views.add_restaurant, name='add_restaurant'),
    url(r'^restaurant/view/$',views.view_restaurant, name='view_restaurant'),
    url(r'^restaurant/delete/(?P<pk>[0-9]+)/$', views.delete_restaurant, name='delete_restaurant'),
    url(r'^restaurant/edit/(?P<pk>[0-9]+)/$', views.edit_restaurant, name='edit_restaurant'),

    url(r'^message/(?P<slug>[\w-]+)/$', views.send_message, name="send_message")
]
