from django.urls import include, path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('pw_change/', views.pw_change, name='pw_change'),
    path('company_list/', views.company_list.as_view(), name='company_list'),
    path('company_add/', views.company_add.as_view(), name='company_add'),
    path('company_update/<int:pk>', views.company_update.as_view(), name='company_update'),
    path('company_detail/<int:pk>', views.company_detail.as_view(), name='company_detail'),
    path('profile_add/<int:cpk>', views.profile_add.as_view(), name='profile_add'),
    path('profile_update/<int:cpk>/<int:pk>', views.profile_update.as_view(), name='profile_update'),
    path('profile_detail/<int:pk>', views.profile_detail.as_view(), name='profile_detail'),
    path('project_list/', views.project_list.as_view(), name='project_list'),
    path('project_add/', views.project_add.as_view(), name='project_add'),
    path('project_update/<int:pk>', views.project_update.as_view(), name='project_update'),
    path('project_detail/<int:pk>', views.project_detail.as_view(), name='project_detail'),
    path('report_list/', views.report_list.as_view(), name='report_list'),
    path('report_add/', views.report_add.as_view(), name='report_add'),
    path('report_update/<int:pk>', views.report_update.as_view(), name='report_update'),
    path('report_detail/<int:pk>', views.report_detail.as_view(), name='report_detail'),
    path('report_check_list/', views.report_check_list.as_view(), name='report_check_list'),
    path('report_check/<int:pk>', views.report_check, name='report_check'),
    path('report_check_detail/<int:pk>', views.report_check_detail.as_view(), name='report_check_detail'),
]
