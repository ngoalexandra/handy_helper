from django.conf.urls import url
from . import views      

urlpatterns = [
    # ----------- templates ---------------
    url(r'^$', views.index), 
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.addJob),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    # -----------process -------------------
    url(r'^process$', views.process), 
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addprocess$', views.add_process),
    url(r'^done/(?P<id>\d+)$', views.done),
    url(r'^view/(?P<id>\d+)$', views.view), 
    url(r'^editprocess$', views.editprocess),  
]

