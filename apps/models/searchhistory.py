
from django.db.models import CharField, Model, DateTimeField


class SearchHistory(Model):
    query = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)