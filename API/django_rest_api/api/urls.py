#-*- coding : utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^category$', views.category, name='category'),
	url(r'^category_list$', views.category_list, name='category_list'),
    url(r'^category/(?P<pid>.{1,})$', views.delete_category, name='delete_category'),
	url(r'^item$', views.item, name='item'),
    url(r'^item/(?P<pid>\d{1,})$', views.delete_item, name='delete_item'),
    url(r'^item/count/(?P<pid>.{1,})/(?P<count>.{1,})$', views.update_count, name='update_count'),
    url(r'^item/limit/(?P<pid>.{1,})/(?P<count>.{1,})$', views.update_limit, name='update_limit'),
]

