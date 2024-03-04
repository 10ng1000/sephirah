from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from .models import Book
import json
from utils.vector_storage import FaissVectorStore
# Create your views here.

class BooksView(View):
    def post(self, request):
        #上传文件
        #multipart/form-data
        file = request.FILES.get('file')
        title = file.name.split('.')[0]
        book = Book.objects.create(title=title, file=file)
        #存储文件向量
        vectorStore = FaissVectorStore(index = str(book.id))
        vectorStore.load_document(doc_path = book.file.path)
        return HttpResponse(json.dumps({'status': 'ok'}))
    
    def get(self, request):
        #获取所有文件
        books = Book.objects.all()
        ret = []
        for book in books:
            ret.append({'title': book.title, 'id': str(book.id), "upload_time": str(book.upload_time)})
        return HttpResponse(json.dumps(ret), content_type='application/json')
        
class SingleBookView(View):
    def post(self, request, id):
        #更新文件
        book = Book.objects.get(id = id)
        file = request.FILES.get('file')
        title = file.name.split('.')[0]
        book.file.delete()
        # 更改为新文件
        book.file = file
        book.title = title
        book.save()
        # 更新文件向量
        vectorStore = FaissVectorStore(index = str(book.id))
        vectorStore.delete()
        vectorStore.load_document(doc_path = book.file.path)
        return HttpResponse(json.dumps({'status': 'ok'}))
    
    def get(self, request, id):
        #获取文件
        book = Book.objects.get(id = id)
        text = book.file.read().decode('utf-8')
        return HttpResponse(json.dumps({'title': book.title, "upload_time": str(book.upload_time), "text": text}), content_type='application/json')
    
    def delete(self, request, id):
        book = Book.objects.get(id = id)
        # 删除文件
        book.file.delete()
        book.delete()
        # 删除文件向量
        vectorStore = FaissVectorStore(index = str(book.id))
        vectorStore.delete()
        return HttpResponse(json.dumps({'status': 'ok'}))
    
    def put(self, request, id):
        #测试，是否能够检索向量
        book = Book.objects.get(id = id)
        vectorStore = FaissVectorStore(index = str(book.id))
        ret = vectorStore.search_with_score("机组调试前要干什么？")

        return HttpResponse(json.dumps({'ret': str(ret)}), content_type='application/json')
