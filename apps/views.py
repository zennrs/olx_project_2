import urllib.parse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
import requests
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from apps.filters import AnnouncementFilterSet
from apps.models import Announcement, Category, User
from django.views.generic import ListView
from apps.models.announcements import ProductImage
from root import settings


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
        context['filter'] = self.filterset
        context['top_categories'] = Category.objects.filter(parent=None)
        return context


class CustomLoginView(LoginView):
    template_name = 'apps/login.html'
    success_url = reverse_lazy('main_page')
    redirect_authenticated_user = True

# class RegisterCreateView(CreateView):
#     template_name = 'apps/auth/register.html'
#     form_class = RegisterModelForm
#     success_url = reverse_lazy('login_page')


class GoogleLoginView(View):
    def get(self, request):
        scope = "email profile"
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?response_type=code"
            f"&client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={urllib.parse.quote(settings.GOOGLE_REDIRECT_URI)}"
            f"&scope={urllib.parse.quote(scope)}"
        )
        return redirect(auth_url)


class GoogleCallbackView(View):
    def get(self, request):
        code = request.GET.get("code")

        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_res = requests.post("https://oauth2.googleapis.com/token", data=token_data).json()
        access_token = token_res.get("access_token")

        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code == 200:
            info = response.json()
            email = info["email"]
            name = info["name"]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={"first_name": name}
            )
            if not user.is_valid_password or created:
                user.set_unusable_password()
                user.save(update_fields=['password'])
            login(request, user)

            return redirect('profile_page')
        return redirect('login_page')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    template_name = 'apps/profile.html'
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('profile_page')

    def get_object(self, queryset=None):
        return self.request.user


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main_page')


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    queryset = Announcement.objects.all()
    template_name = 'apps/add.html'
    fields = ['name', 'description', 'category', 'price']
    MAX_IMAGES = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_categories'] = Category.objects.filter(parent=None)
        return context

    def form_valid(self, form):
        images = self.request.FILES.getlist("images")

        if len(images) > self.MAX_IMAGES:
            form.add_error(None, f"Можно загрузить максимум {self.MAX_IMAGES} фото.")
            return self.form_invalid(form)

        response = super().form_valid(form)

        for i, img in enumerate(images):
            ProductImage.objects.create(product=self.object, image=img, order=i)

        return response
