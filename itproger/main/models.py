from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    annotation = models.TextField(blank=True)
    publication_date = models.DateField(blank=True, null=True)
    cover_link = models.URLField(blank=True)
    detail_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

class ReadBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'book')

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author.username} к "{self.book.title}"'