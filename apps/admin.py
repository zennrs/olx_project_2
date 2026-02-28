from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.models.categories import ManufactureCategory,Category,Manufacturer
from apps.models.announcements import Announcement,AnnouncementImage


# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }



class AnnouncementImageTabularInline(TabularInline):
    model = AnnouncementImage
    min_num = 1
    extra = 0


@admin.register(Announcement)
class AnnouncementModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = AnnouncementImageTabularInline,





@admin.register(Manufacturer)
class ManufacturerModelAdmin(ModelAdmin):
    pass


@admin.register(ManufactureCategory)
class ManufactureCategoryModelAdmin(ModelAdmin):
    pass
