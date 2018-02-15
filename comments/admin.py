from django.contrib import admin
from comments.models import NoticeComment, MenuComment, ReviewComment


admin.site.register(NoticeComment)

admin.site.register(MenuComment)

admin.site.register(ReviewComment)