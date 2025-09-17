from django.contrib import admin
from .models import Group, Post, Comment, Follow


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "pub_date", "group")
    list_filter = ("pub_date", "group")
    search_fields = ("text", "author__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created")
    list_filter = ("created",)
    search_fields = ("text", "author__username")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "following")
    search_fields = ("user__username", "following__username")
