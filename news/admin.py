from django.contrib import admin
from .models import Author, Category, Post,  Comment
from django import forms






@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_sender', 'text',  'dateCreation', 'active')
    list_filter = ('active', 'dateCreation')
    search_fields = ('user_sender',  'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
# admin.site.register(Comment)


