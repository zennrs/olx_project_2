from unicodedata import category

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView

from apps.filters import AnnouncementFilterSet
from apps.models import Announcement, Category


from django.views.generic import ListView

class MainView(ListView):
    template_name = 'apps/main.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(parent=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.filter(product_type="vip")
        return context


class AnnouncementListView(ListView):
    template_name = 'apps/announcement-list.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=slug)
        queryset = Announcement.objects.filter(category=category)
        self.filterset = AnnouncementFilterSet(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем категории верхнего уровня отдельно
        context['filter'] = self.filterset
        context['top_categories'] = Category.objects.filter(parent=None)
        return context





class TestView(ListView):
    template_name = 'apps/login.html'
    queryset = Category.objects.all()