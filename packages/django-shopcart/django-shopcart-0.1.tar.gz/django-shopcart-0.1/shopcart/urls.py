from django.conf.urls import url

from . import views

app_name = 'shopcart'
urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^bill/$', views.checkout, name='checkout'),
    url(r'^invoice/$', views.invoice, name='invoice'),
]
