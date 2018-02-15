from django.db import models


class Store(models.Model):
    shopkeeper = models.ForeignKey('auth.User', related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locations = models.TextField()
    phone = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(default='media/default_image.png')
    # category
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} == {}".format(self.shopkeeper.username, self.name)

    @property
    def owner(self):
        return self.shopkeeper


class LikeManeger(models.Manager):
    def toggle_like(self, request_user, notice_to_toggle):
        notice_ = Notice.objects.get(notice=notice_to_toggle)
        user = request_user
        like_notice = False
        if user in notice_.like_user.all():
            notice_.like_user.remove(user)
        else:
            notice_.like_user.add(user)
            like_notice = True
        return notice_, like_notice


class Notice(models.Model):
    title = models.CharField(max_length=100, default='notice')
    text = models.TextField()
    # like
    # hit
    image = models.ImageField(default='media/default_image.png')
    # category
    store = models.ForeignKey('Store', related_name='notice', on_delete=models.CASCADE)
    like_user = models.ManyToManyField('auth.User', related_name='like_notice', blank=True)

    @property
    def owner(self):
        return self.store.shopkeeper
