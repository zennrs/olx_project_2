from django.db.models import CharField, CASCADE, ManyToManyField, ForeignKey, JSONField, TextChoices, Model
from django.db.models.fields import PositiveIntegerField, PositiveSmallIntegerField, TextField, EmailField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from apps.models.base import ImageBaseModel, SlugBaseModel, CreatedBaseModel
from root.settings import AUTH_USER_MODEL


# class Category(SlugBaseModel, ImageBaseModel, MPTTModel):
#     name = CharField(max_length=255)
#     parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
#     manufacturers = ManyToManyField('apps.Manufacturer',
#                                     through='apps.ManufactureCategory',
#                                     related_name='categories')
#     attribute = JSONField(blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class MPTTMeta:
#         order_insertion_by = ['name']
#
#
# class Manufacturer(CreatedBaseModel, SlugBaseModel, ImageBaseModel):
#     name = CharField(max_length=255)
#     attribute = JSONField(blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class ManufactureCategory(Model):
#     manufacturer = ForeignKey('apps.Manufacturer', CASCADE, to_field='slug')
#     category = ForeignKey('apps.Category', CASCADE, to_field='slug')


class Announcement(SlugBaseModel, CreatedBaseModel):
    class AnnouncementType(TextChoices):
        SIMPLE = "simple", "SIMPLE"
        VIP = "vip", "VIP"


    class Status(TextChoices):
        Active = 'active', 'Active'
        Expected = 'expected', 'Expected'
        Unpaid = 'unpaid', 'Unpaid'
        Unactive = 'unactive', 'Unactive'

    name = CharField(max_length=255)
    price = PositiveIntegerField()
    discount = PositiveSmallIntegerField(db_default=0)
    description = TextField(blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    product_type = CharField(max_length=10, choices=AnnouncementType.choices, default=AnnouncementType.SIMPLE)
    attribute = JSONField(blank=True, null=True)
    owner = ForeignKey(AUTH_USER_MODEL, related_name='announcements',on_delete=CASCADE)
    status = CharField(max_length=10, choices=Status.choices, default=Status.Unactive)
    view_count = PositiveIntegerField(default=0)
    email = EmailField(blank=True, null=True)
    phone = CharField(max_length=15, blank=True, null=True)
    favorites = ManyToManyField(
        AUTH_USER_MODEL,
        related_name="favorite_products",
        blank=True
    )



    @property
    def first_image(self):
        return self.favorites.count()
        # img = self.images.first()
        # if img:
        #     return img.image.url
        # return None


class AnnouncementImage(ImageBaseModel):
    product = ForeignKey('apps.Announcement', CASCADE, related_name='images')
