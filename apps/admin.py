from django.contrib.admin import ModelAdmin
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from apps.models import Category, Announcement, Manufacturer
from apps.models.announcements import ManufactureCategory


# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Announcement)
class AnnouncementModelAdmin(ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerModelAdmin(ModelAdmin):
    pass


@admin.register(ManufactureCategory)
class ManufactureCategoryModelAdmin(ModelAdmin):
    pass
