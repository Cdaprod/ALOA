from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('network_mapping/', views.network_mapping, name='network_mapping'),
    path('device_enumeration/', views.device_enumeration, name='device_enumeration'),
    path('traffic_sniffing/', views.traffic_sniffing, name='traffic_sniffing'),
    path('active_scanning/', views.active_scanning, name='active_scanning'),
    path('passive_scanning/', views.passive_scanning, name='passive_scanning'),
    path('mitm_attacks/', views.mitm_attacks, name='mitm_attacks'),
    path('command_and_control/', views.command_and_control, name='command_and_control'),
    path('dynamic_payload_generation/', views.dynamic_payload_generation, name='dynamic_payload_generation'),
    path('lateral_movement_automation/', views.lateral_movement_automation, name='lateral_movement_automation'),
    path('custom_encryption/', views.custom_encryption, name='custom_encryption'),
    path('traffic_mimicry/', views.traffic_mimicry, name='traffic_mimicry'),
    path('deception/', views.deception, name='deception'),
    path('machine_learning/', views.machine_learning, name='machine_learning'),
]
