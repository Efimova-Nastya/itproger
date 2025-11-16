from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from django import forms
from .models import Book, ReadBook, Comment

# Форма комментария
class CommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите ваш комментарий...'}),
        label="Ваш комментарий"
    )

# Главная страница
def main_page(request):
    books = Book.objects.select_related('author').all()
    query = request.GET.get('q', '').strip()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    sort = request.GET.get('sort', 'title')
    valid_sorts = ['title', '-title', 'author__name', '-author__name', 'publication_date', '-publication_date']
    if sort in valid_sorts:
        books = books.order_by(sort)
    if request.user.is_authenticated:
        read_ids = ReadBook.objects.filter(user=request.user, read=True).values_list('book_id', flat=True)
        for book in books:
            book.is_read = book.id in read_ids
    else:
        for book in books:
            book.is_read = False
    return render(request, 'main/main.html', {'books': books})

# Детальная страница книги
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    read_status = False
    if request.user.is_authenticated:
        read_obj, _ = ReadBook.objects.get_or_create(user=request.user, book=book, defaults={'read': False})
        read_status = read_obj.read
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                Comment.objects.create(book=book, author=request.user, text=form.cleaned_data['text'])
                messages.success(request, "Комментарий добавлен!")
                return redirect('book_detail', book_id=book.id)
        else:
            form = CommentForm()
    else:
        form = None
    comments = book.comments.select_related('author').all()
    return render(request, 'main/book_detail.html', {
        'book': book,
        'read_status': read_status,
        'form': form,
        'comments': comments,
    })

# Переключить "прочитано"
@login_required
def toggle_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    read_obj, _ = ReadBook.objects.get_or_create(user=request.user, book=book, defaults={'read': False})
    read_obj.read = not read_obj.read
    read_obj.save()
    return redirect('book_detail', book_id=book.id)

# Страница статистики
@login_required
def read_books_page(request):
    count = ReadBook.objects.filter(user=request.user, read=True).count()
    read_books = ReadBook.objects.filter(user=request.user, read=True).select_related('book__author')
    return render(request, 'main/read_books.html', {'count': count, 'read_books': read_books})

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

# Редактировать комментарий
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот комментарий.")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['text']
            comment.save()
            messages.success(request, "Комментарий обновлён.")
            return redirect('book_detail', book_id=comment.book.id)
    else:
        form = CommentForm(initial={'text': comment.text})
    return render(request, 'main/edit_comment.html', {'form': form, 'comment': comment})

# Удалить комментарий
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий.")
    if request.method == 'POST':
        book_id = comment.book.id
        comment.delete()
        messages.success(request, "Комментарий удалён.")
        return redirect('book_detail', book_id=book_id)
    return render(request, 'main/delete_comment.html', {'comment': comment})