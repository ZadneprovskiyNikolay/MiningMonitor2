from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index),
    path('add-device/', views.add_device),    
    path('my-devices/', views.my_devices),    
    path('devices/my_devices.json', views.my_devices_json), 
    path('add-transaction/', views.add_transaction),     
    path('maintenance/', views.maintenance),   
    path('manage-devices/', views.manage_devices),
    path('work-archive/', views.work_archive),
    path('work-archive/<int:device_id>/work_archive.json', views.work_archive_json),
    path('archive-devices/', views.archive_devices),
    path('devices/archive_devices.json', views.archive_devices_json),
    path('payback/', views.payback),
    path('payback/<int:device_id>/payback.json', views.payback_json),
    path('transactions/', views.transactions),
    path('transactions/transactions.json', views.transactions_json),
]
