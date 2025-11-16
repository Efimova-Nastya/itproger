from .models import ReadBook

def unread_books_count(request):
    read_count = 0
    if request.user.is_authenticated:
        read_count = ReadBook.objects.filter(user=request.user, read=True).count()
    return {'read_count': read_count}