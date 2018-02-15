from django.db import models
from stores.models import Notice


class NoticeComment(models.Model):
    #id
    # qs = Notice.objects.all()
    # print(qs)
    text = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', related_name='notice_comment_user', on_delete=models.CASCADE)
    notice = models.ForeignKey('stores.Notice', related_name='notice_comment', on_delete=models.CASCADE)
    like = models.ManyToManyField('auth.User', related_name='notice_comment_like')

    def __str__(self):
        return "{}::{}".format(self.user.usernamem, self.notice.title)


class MenuComment(models.Model):
    #id
    text = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', related_name='menu_comment_user', on_delete=models.CASCADE)
    menu = models.ForeignKey('menus.Menu', related_name='menu_comment', on_delete=models.CASCADE)
    like = models.ManyToManyField('auth.User', related_name='menu_comment_like')

    def __str__(self):
        return "{}::{}".format(self.user.usernamem, self.notice.title)

    @property
    def owner(self):
        return self.user


class ReviewComment(models.Model):
    #id
    text = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', related_name='review_comment_user', on_delete=models.CASCADE)
    review = models.ForeignKey('menus.Review', related_name='review_comment', on_delete=models.CASCADE)
    like = models.ManyToManyField('auth.User', related_name='review_comment_like')

    def __str__(self):
        return "{}::{}".format(self.user.usernamem, self.notice.title)

    @property
    def owner(self):
        return self.user