from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('availability', views.availability, name='availability'),
    path('availabilitysaved', views.availabilitysaved, name='availabilitysaved'),
    path('schedule/<int:year>/<int:month>', views.schedule, name='schedule'),
    #path('schedule', views.schedule, name='schedule'),
    path('schedulemaker', views.schedulemaker, name='schedulemaker'),
    path('schedulemaker/<int:forday>', views.schedulemaker, name='schedulemaker'),
    path('schedulesaved/<int:forday>', views.schedulesaved, name='schedulesaved')
]