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
        return HttpResponse('ok')
    
    def get(self, request):
        books = Book.objects.all()
        return HttpResponse(json.dumps([{'title': book.title, 'id': book.id, "upload_time": str(book.upload_time)} for book in books]), content_type='application/json')
        
class SingleBookView(View):
    def put(self, request, id):
        try:
            book = Book.objects.get(id = id)
            file = request.FILES.get('file')
            book.file.delete()
            book.file = file
            book.save()
            return HttpResponse('ok')
        except:
            return HttpResponseNotFound('no content')
    
    def get(self, request, id):
        try:
            book = Book.objects.get(id = id)
            print(book.file.name)
            text = book.file.read().decode('utf-8')
            print(str(text))
            return HttpResponse(json.dumps({'title': book.title, "upload_time": str(book.upload_time), "text": text}), content_type='application/json')
        except:
            return HttpResponseNotFound('no content')
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(id = id)
            # 删除文件
            book.file.delete()
            book.delete()
            return HttpResponse('ok')
        except:
            return HttpResponse('no content', status=204)