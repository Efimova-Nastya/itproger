from django.contrib import admin
from .models import Book, Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    fields = (
        'title',
        'author',
        'cover',
        'publication_date',
        'annotation',
        'cover_link',
        'detail_link'
    )