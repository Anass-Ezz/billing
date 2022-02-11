from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path('', views.billing, name='billing'),
    path('login', views.login_view, name='login_view'),
    path('test_pdf', views.test_pdf, name='test_pdf'),
    path('bill_summary', views.bill_summary, name='bill_summary'),
    path('item_details/<int:id>/', views.detail, name='detail'),
    path('add_item/', views.add_item, name='add_item'),
    path('remove_item/<int:id>/', views.remove_item, name='remove_item'),
    path('set_price', views.set_price, name='set_price'),
    path('set_discount', views.set_discount, name='set_discount'),
    path('finish_order', views.finish_order, name='finish_order'),
    path('set_quantity',
         views.set_quantity, name='set_quantity'),
    path('view_client',
         views.view_client, name='view_client'),
    path('set_client',
         views.set_client, name='set_client'),
    path('search_client', views.search_client, name='search_client'),
    path('add_client', views.add_client, name='add_client'),
    #     path('product_search', views.product_search, name='product_search'),
]
