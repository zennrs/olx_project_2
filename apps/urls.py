from django.urls import path
from apps.views import ProductListView, CategoryLIstView, MainView

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='product_list_page'),
]
