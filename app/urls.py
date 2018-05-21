from django.conf.urls import url
from app import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('upload/', views.upload_pic, name='upload')
]
