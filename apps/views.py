from unicodedata import category

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from apps.models import Product, Category


from django.views.generic import ListView

class MainView(ListView):
    template_name = 'apps/main.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(parent=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:10]
        return context


class ProductListView(ListView):
    template_name = 'apps/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=slug)
        return Product.objects.filter(category=category)

class CategoryLIstView(ListView):
    queryset = Category.objects.all()
    # template_name = 'apps/main.html'
    context_object_name = 'category'



