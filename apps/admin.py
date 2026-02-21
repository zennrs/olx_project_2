from django.contrib import admin

from apps.models import Category, Announcement


# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass





@admin.register(Announcement)
class AnnouncementModelAdmin(admin.ModelAdmin):
    pass
