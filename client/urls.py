from django.urls import path

from client import views

urlpatterns = [
    path('order/', views.index, name='index2'),
    path('order/success/', views.order_success, name='order_success'),
    path('order/search/', views.order_search, name='order_search'),
    path('order/search/err', views.search_err, name='search_err'),
    path('order/search/<int:client_id>', views.order_accept, name='order_accept'),
    path('select/', views.client_select, name='select_accept_order'),
    path('blacklist/', views.black_list, name='black_list'),
    path('blacklist/<int:client>', views.black_list_err, name='black_list_err'),
    path('blacklist/info/<int:client_id>', views.black_list_info, name='black_list_info'),
    path('blacklist/add/<int:client_id>', views.black_list_add, name='black_list_add'),
    path('additional_order/search/', views.additional_order_search, name='additional_order_search'),
    path('additional_order/<int:client_id>', views.additional_order, name='additional_order'),
    path('additional_order/search/err', views.additional_search_err, name='additional_search_err'),
    path('additional_order/sucess/<int:client_id>', views.additional_order_success, name='additional_order_success'),
    path('additional_order/err', views.additional_err, name='additional_err'),
    path('rest/', views.restaurant_select, name='restaurant_select'),
    path('rest/order/', views.restaurant_order, name='restaurant_order'),
    path('rest/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('rest/menu/succ', views.restaurant_menu_success, name='restaurant_menu_success'),
    path('rest/menu/err', views.restaurant_menu_err, name='restaurant_menu_err'),
]