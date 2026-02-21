from django.urls import path
from apps.views import AnnouncementListView, MainView, TestView

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('category/<slug:slug>/', AnnouncementListView.as_view(), name='announcement_list_page'),
    path('login/', TestView.as_view(), name='login_page'),
]
