from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from .models import Book
import json
# Create your views here.

class BooksView(View):
    def post(self, request):
        #multipart/form-data
        file = request.FILES.get('file')
        title = file.name.split('.')[0]
        book = Book.objects.create(title=title, file=file)
        return HttpResponse(json.dumps({'status': 'ok'}))
    
    def get(self, request):
        books = Book.objects.all()
        return HttpResponse(json.dumps([{'title': book.title, 'id': str(book.id), "upload_time": str(book.upload_time)} for book in books]), content_type='application/json')
        
class SingleBookView(View):
    def post(self, request, id):
        book = Book.objects.get(id = id)
        file = request.FILES.get('file')
        title = file.name.split('.')[0]
        book.file.delete()
        # 更改为新文件
        book.file = file
        book.title = title
        book.save()
        return HttpResponse(json.dumps({'status': 'ok'}))
    
    def get(self, request, id):
        book = Book.objects.get(id = id)
        text = book.file.read().decode('utf-8')
        return HttpResponse(json.dumps({'title': book.title, "upload_time": str(book.upload_time), "text": text}), content_type='application/json')

    
    def delete(self, request, id):
        book = Book.objects.get(id = id)
        # 删除文件
        book.file.delete()
        book.delete()
        return HttpResponse(json.dumps({'status': 'ok'}))

class BookSessionView(View):
    def post(self, request, id):
        book = Book.objects.get(id = id)
        chat_session_id = json.loads(request.body.decode('utf-8'))['chat_session_id']
        book.chat_sessions.add(chat_session_id)
        return HttpResponse(json.dumps({'status': 'ok'}))