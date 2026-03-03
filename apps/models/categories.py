from django.db.models import CharField, ForeignKey, JSONField, CASCADE, Model, ManyToManyField
from mptt.models import MPTTModel

from apps.models.base import SlugBaseModel, ImageBaseModel, CreatedBaseModel


class Category(SlugBaseModel, ImageBaseModel, MPTTModel):
    name = CharField(max_length=255)
    parent = ForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
    manufacturers = ManyToManyField('apps.Manufacturer',
                                    through='apps.ManufactureCategory',
                                    related_name='categories')
    attribute = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']



class Manufacturer(CreatedBaseModel, SlugBaseModel, ImageBaseModel):
    name = CharField(max_length=255)
    attribute = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class ManufactureCategory(Model):
    manufacturer = ForeignKey('apps.Manufacturer', CASCADE, to_field='slug')
    category = ForeignKey('apps.Category', CASCADE, to_field='slug')