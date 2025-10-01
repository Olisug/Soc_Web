from django.contrib import admin
from .models import Profile, Follower, Friend


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'short_name', 'city', 'birth_date', 'email')
    fields = ('username',
              'avatar',
              'short_name',
              'gender',
              'city',
              'birth_date',
              'email',)
    search_fields = ('username',)
    ordering = ('username',)


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower_for')
    search_fields = ('user',)
    ordering = ('user',)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'users_friend', 'confirmed')
    search_fields = ('user', 'users_friend', 'confirmed')
    ordering = ('user', 'users_friend', 'confirmed')