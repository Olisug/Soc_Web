from django.contrib import admin

from .models import Posts, Likes


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'author', 'pub_time')
    search_fields = ('author__username',)
    ordering = ('author',)

    def short_text(self, obj):
        """Сокращенный текст для отображения в админке"""
        if obj.text:
            return obj.text[:20] + '...' if len(obj.text) > 10 else obj.text
        return '-'


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('maker', 'for_post')
    search_fields = ('maker__username',)
    ordering = ('maker__username',)