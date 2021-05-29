from django.urls import path
from django.contrib.auth import views as auth_views

from reg import views

urlpatterns = [
    path('reg/', views.index, name='index1'),
    path('reg/oops/', views.bad_page, name='bad_page'),
    path('reg/aops/', views.bad_auth, name='bad_auth'),
    path('reg/success/', views.suc_registration, name='suc_registration'),
    path('test/', views.test, name='test'),
    path('auth/', views.auth, name='auth'),
    path('vacations/search/', views.search_worker_for_vacations, name='search_worker_for_vacations'),
    path('vacations/search/Err', views.worker_search_err, name='worker_search_err'),
    path('vacations/search/<int:worker_id>', views.vacations_for_worker, name='vacations_for_worker'),
    path('vacations/success/', views.worker_vacation_success, name='worker_vacation_success'),
    path('', views.select, name='select'),
]
