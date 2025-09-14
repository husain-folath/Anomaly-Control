from django.urls import path
from . import views

urlpatterns = [
    # Home & About
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),

    # Entities
    path('entities/', views.entity_index, name='entity_index'),
    path('entities/<int:entity_id>/', views.entity_detail, name='entity_detail'),
    path('entities/create/', views.EntityCreate.as_view(), name='entity_create'),
    path('entities/<int:pk>/update/', views.EntityUpdate.as_view(), name='entity_update'),
    path('entities/<int:pk>/delete/', views.EntityDelete.as_view(), name='entity_delete'),

    # # Reports
    # path('reports/', views.report_index, name='report_index'),
    # path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    # path('reports/create/', views.ReportCreate.as_view(), name='report_create'),
    # path('reports/<int:pk>/update/', views.ReportUpdate.as_view(), name='report_update'),
    # path('reports/<int:pk>/delete/', views.ReportDelete.as_view(), name='report_delete'),

    # # Incidents
    # path('incidents/', views.incident_index, name='incident_index'),
    # path('incidents/<int:incident_id>/', views.incident_detail, name='incident_detail'),
    # path('incidents/create/', views.IncidentCreate.as_view(), name='incident_create'),
    # path('incidents/<int:pk>/update/', views.IncidentUpdate.as_view(), name='incident_update'),
    # path('incidents/<int:pk>/delete/', views.IncidentDelete.as_view(), name='incident_delete'),

    # # Authentication
    path('accounts/signup/', views.signup, name='signup'),
]
