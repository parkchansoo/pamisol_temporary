from django.db import models
from stores.models import Store


class Menu(models.Model):
    #id
    name = models.CharField(max_length=40, default='default menu')
    description = models.TextField()
    image = models.ImageField(default='media/default_image.png')
    price = models.IntegerField()
    #category
    #like
    #hit
    #grade
    store = models.ForeignKey('stores.Store', related_name='menu', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.store.shopkeeper


class Review(models.Model):
    #id
    text = models.TextField()
    image = models.ImageField(default='media/default_image.png')
    # like
    # hit
    # grade
    user = models.ForeignKey('auth.User', related_name='user_review', on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu', related_name='menu_review', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def owner(self):
        return self.user