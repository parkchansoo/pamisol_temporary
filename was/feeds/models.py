from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from customprofile.models import UserProfile


class StoreFeed(models.Model):
    store = models.ForeignKey('stores.Store', related_name='storefeed', on_delete=models.CASCADE, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    storefeed_object = GenericForeignKey('content_type', 'object_id')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.store) + " - " +str(self.store.menu.name)