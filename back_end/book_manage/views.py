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
        return HttpResponse(json.dumps([{'title': book.title, 'id': book.id} for book in books]), content_type='application/json')
        
class SingleBookView(View):
    def get(self, request, id):
        try:
            book = Book.objects.get(id = id)
            return HttpResponse(json.dumps({'title': book.title}), content_type='application/json')
        except:
            return HttpResponse('no content', status=204)
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(id = id)
            # 删除文件
            book.file.delete()
            book.delete()
            return HttpResponse('ok')
        except:
            return HttpResponse('no content', status=204)