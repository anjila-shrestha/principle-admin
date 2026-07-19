from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('complaints/', views.all_complaints, name='all_complaints'),
    path('analytics/', views.analytics, name='analytics'),
    path('users/', views.user_management, name='user_management'),
    path('complaints/<str:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaints/<str:complaint_id>/reveal/', views.reveal_identity, name='reveal_identity'),
    path('audit-log/', views.audit_log_view, name='audit_log'),
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_complaints_csv, name='export_csv'),
]