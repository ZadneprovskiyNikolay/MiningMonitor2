from django.urls import path
from graphene_django.views import GraphQLView
from monitor.schema import schema

from . import views

urlpatterns = [ 
    path('', views.index),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('add-device/', views.add_device),    
    path('my-devices/', views.my_devices),    
    path('add-transaction/', views.add_transaction_view),     
    path('maintenance/', views.maintenance),   
    path('manage-devices/', views.manage_devices),
    path('work-archive/', views.work_archive),
    path('work-archive/<int:device_id>/work_archive.json', views.work_archive_json),
    path('archive-devices/', views.archive_devices),
    path('payback/', views.payback),
    path('payback/<int:device_id>/payback.json', views.payback_json),
    path('transactions/', views.transactions),
]
