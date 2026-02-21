from django.core.validators import FileExtensionValidator
from django.db.models import ImageField, CharField, CASCADE, ManyToManyField, \
    ForeignKey, JSONField, TextChoices
from django.db.models.fields import PositiveIntegerField, PositiveSmallIntegerField, TextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.models.base import ImageBaseModel, SlugBaseModel, CreatedBaseModel
from apps.models.utils import upload_image_size_5mb_validator


class Category(SlugBaseModel, ImageBaseModel, MPTTModel):
    name = CharField(max_length=255)
    banner = ImageField(upload_to='categories/banner/%Y/%m/%d',
                        validators=[FileExtensionValidator(['jpeg', 'jpg', 'png', 'webp']),
                                    upload_image_size_5mb_validator],
                        help_text='jpg, png, webp are allowed', blank=True, null=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
    manufacturers = ManyToManyField('apps.Manufacturer', through='apps.ManufactureCategory', related_name='categories')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Announcement(SlugBaseModel, CreatedBaseModel):
    class AnnouncementType(TextChoices):
        SIMPLE = "simple", "SIMPLE"
        VIP = "vip", "VIP"


    name = CharField(max_length=255)
    price = PositiveIntegerField()
    discount = PositiveSmallIntegerField(db_default=0)
    specification = JSONField(default=dict, blank=True)
    description = TextField(blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    product_type = CharField(max_length=10, choices=AnnouncementType.choices, default=AnnouncementType.SIMPLE)

    @property
    def first_image(self):
        return self.favorites.count()
        # img = self.images.first()
        # if img:
        #     return img.image.url
        # return None


class ProductImage(ImageBaseModel):
    product = ForeignKey('apps.Announcement', CASCADE, related_name='images')
