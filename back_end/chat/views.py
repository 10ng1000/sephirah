from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from utils.zhipu_llm import ZhipuLLMWithMemory, ZhipuLLMWithRetrieval
from chat.models import ChatSession
from utils.memory import RedisMemory
import json

# Create your views here.
class ChatSseView(View):
    def post(self, request):
        '''sse请求LLM，在聊天页面使用'''
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        if not session_id:
            return HttpResponseBadRequest("session_id is required")
        zhipuLLM = ZhipuLLMWithMemory(session_id=session_id)
        def event_stream():
            for chunk in zhipuLLM.stream(message):
                yield f'data: {json.dumps({"message" : chunk, "end": False})}\n\n'
            yield f'data: {json.dumps({"message" : "", "end": True})}\n\n'
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

class ChatRetrievalView(View):
    def post(self, request):
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        k = data.get('k')
        from utils.vector_storage import FaissVectorStore
        linked_books = ChatSession.objects.get(session_id=session_id).linked_books.all()
        if not linked_books:
            #todo 前端做相应提示
            return HttpResponseBadRequest("linked_books is required")
        related_docs = []
        for book in linked_books:
            faiss = FaissVectorStore(str(book.id))
            related_docs.extend(faiss.search_with_score(message))
        #按照得分排序，取得分最低的k个
        related_docs.sort(key=lambda x: x[1])
        related_docs = related_docs[:k]
        zhipuLLM = ZhipuLLMWithRetrieval(related_docs,session_id, k)
        def event_stream():
            for chunk in zhipuLLM.stream(message):
                yield f'data: {json.dumps({"message" : chunk, "end": False})}\n\n'
            yield f'data: {json.dumps({"message" : "", "end": True})}\n\n'
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        #return HttpResponse(json.dumps({'text': zhipuLLM.invoke(message)}))

class ChatView(View):
    def post(self, request):
        '''暂时弃用'''
        data = json.loads(request.body)
        message = data.get('message')
        return HttpResponse(json.dumps({'text': self.zhipuLLM().invoke(message)}))

class ChatSessionView(View):
    def get(self, request, session_id):
        # 获取一个大模型对话session
        session = ChatSession.objects.get(session_id=session_id)
        books = session.linked_books.all()
        #获得redis中session对应的聊天记录
        memory = RedisMemory(session_id=session_id)
        history = memory.get_history()
        return HttpResponse(json.dumps({'session_id': str(session.session_id), 'name': session.name, 'start_time': str(session.start_time), 'history': history, 'books': [{'id': str(book.id), 'title': book.title} for book in books]}))

    def delete(self, request, session_id):
        # 删除一个大模型对话session
        session = ChatSession.objects.get(session_id=session_id)
        session.delete()
        return HttpResponse(json.dumps({'status': 'success'}))
        
class ChatSessionsView(View):
    def post(self, request):
        # 创建一个新的大模型对话session
        # 使用时间戳加随机数作为session_id
        import time
        import secrets
        name = json.loads(request.body).get('message')
        session_id = f'{int(time.time())}-{secrets.token_hex(8)}'
        #把id存入数据库
        session = ChatSession(session_id=session_id, name=name)
        session.save()
        linked_books = json.loads(request.body).get('linked_books')
        if linked_books:
            for book_id in linked_books:
                session.linked_books.add(book_id)
        return HttpResponse(json.dumps({'session_id': session_id}))

    def get(self, request):
        # 获取所有大模型对话session，按时间顺序排序
        sessions = ChatSession.objects.all().order_by('-start_time')
        return HttpResponse(json.dumps(
            [{'session_id': str(session.session_id), 'name': session.name,'start_time': str(session.start_time)} for session in sessions]
        ))
    
class ChatSessionBooksView(View):
    def post(self, request, session_id):
        # 为一个大模型对话session添加一本书
        book_id = json.loads(request.body).get('book_id')
        session = ChatSession.objects.get(session_id=session_id)
        session.linked_books.add(book_id)
        return HttpResponse(json.dumps({'status': 'success'}))

    def get(self, request, session_id):
        # 获取一个大模型对话session的所有书id
        session = ChatSession.objects.get(session_id=session_id)
        books = session.linked_books.all()
        return HttpResponse(json.dumps([{'id': str(book.id)} for book in books]))

    def delete(self, request, session_id, book_id):
        # 删除一个大模型对话session的某一本书
        session = ChatSession.objects.get(session_id=session_id)
        book = session.linked_books.get(id=book_id)
        session.linked_books.remove(book)
        return HttpResponse(json.dumps({'status': 'success'}))