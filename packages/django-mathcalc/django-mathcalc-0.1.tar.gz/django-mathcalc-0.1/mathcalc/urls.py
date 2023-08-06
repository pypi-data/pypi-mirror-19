from django.conf.urls import url

from . import views

app_name = 'mathcalc'
urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^choice/$', views.select_choice, name='select_choice'),
    url(r'^area-circle/$', views.area_circle, name='area_circle'),
    url(r'^perimeter-rectangle/$', views.perimeter_rectangle, name='perimeter_rectangle')
]
