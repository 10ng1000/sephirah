from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from utils.zhipu_llm import ZhipuLLMWithMemory, ZhipuLLMWithRetrieval, ZhipuLLMWithMemoryWebSearch, ZhipuLLMWithWebSearch
from chat.models import ChatSession, ChatMessage
from chat.models import RoleSetting
from utils.memory import RedisMemory
import json
from dotenv import load_dotenv
import os


class ChatRoleSettingView(View):
    def post(self, request):
        data = json.loads(request.body)
        setting = data.get('setting')
        #删除原有的记录
        if RoleSetting.objects.all():
            RoleSetting.objects.all().delete()
        role_setting = RoleSetting(setting=setting)
        role_setting.save()
        return HttpResponse(json.dumps({'status': 'success'}))
    
    def get(self, request):
        role_setting = RoleSetting.objects.all()
        if not role_setting:
            return HttpResponse(json.dumps({'setting': None}))
        return HttpResponse(json.dumps({'setting': role_setting[0].setting}))

    def delete(self, request):
        if RoleSetting.objects.all():
            RoleSetting.objects.all().delete()
        return HttpResponse(json.dumps({'status': 'success'}))

# Create your views here.
class ChatSseView(View):
    def post(self, request):
        '''sse请求LLM，在聊天页面使用'''
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        if not session_id:
            return HttpResponseBadRequest("session_id is required")
        if RoleSetting.objects.all():
            role_setting = RoleSetting.objects.all()[0].setting
        else:
            role_setting = None
        zhipuLLM = ZhipuLLMWithMemory(session_id=session_id, role=role_setting)
        def event_stream():
            for chunk in zhipuLLM.stream(message):
                yield f'data: {json.dumps({"message" : chunk, "end": False})}\n\n'
            yield f'data: {json.dumps({"message" : "", "end": True})}\n\n'
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    
class ChatWebSearchView(View):
    def post(self, request):
        '''sse请求LLM，附带网页搜索功能，在聊天页面使用'''
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        #由于是先提取历史，再调用LLM，所以index为历史长度
        current_index = data.get('index')
        if not session_id:
            return HttpResponseBadRequest("session_id is required")
        if RoleSetting.objects.all():
            role_setting = RoleSetting.objects.all()[0].setting
        else:
            role_setting = None
        zhipuLLM = ZhipuLLMWithWebSearch(session_id=session_id, role=role_setting)
        def event_stream():
            for chunk in zhipuLLM.stream(message):
                if len(chunk) >= 30 and chunk.startswith("[{'title':"):
                    #把搜索结果保存到django后端
                    session = ChatSession.objects.get(session_id=session_id)
                    ChatMessage(session=session, web_search_results=chunk, index=current_index).save()
                    #测试是否保存成功，获得session_id为当前id，index为当前index的记录
                    yield f'data: {json.dumps({"message" : chunk, "end": True, "is_retrieval":False})}\n\n'
                else:
                    yield f'data: {json.dumps({"message" : chunk, "end": False})}\n\n'
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        
class ChatRetrievalView(View):
    def post(self, request):
        data = json.loads(request.body)
        message = data.get('message')
        session_id = data.get('session_id')
        current_index = data.get('index')
        k = int(os.getenv('RETRIEVAL_K'))
        from utils.vector_storage import FaissVectorStore
        linked_books = ChatSession.objects.get(session_id=session_id).linked_books.all()
        if not linked_books:
            return HttpResponseBadRequest("linked_books is required")
        related_docs = []
        for book in linked_books:
            # print(book.id)
            faiss = FaissVectorStore(str(book.id))
            related_docs.extend(faiss.search_with_score(message))
        #按照得分排序，取得分最低的k个
        related_docs.sort(key=lambda x: x[1])
        related_docs = related_docs[:k]
        #如果有role设置，使用role设置
        if RoleSetting.objects.all():
            role_setting = RoleSetting.objects.all()[0].setting
        else:
            role_setting = None
        zhipuLLM = ZhipuLLMWithRetrieval(related_docs,session_id, k, role=role_setting)
        def event_stream():
            for chunk in zhipuLLM.stream(message):
                yield f'data: {json.dumps({"message" : chunk, "end": False})}\n\n'
            doc = [{'title': document.page_content, 'media': document.metadata['source'].split('/')[-1].split('.')[0]} for document, score in related_docs]
            #将结果保存到后端
            session = ChatSession.objects.get(session_id=session_id)
            ChatMessage(session=session, web_search_results=json.dumps(doc), index=current_index, is_retrieval=True).save()
            yield f'data: {json.dumps({"message" : str(doc), "end": True, "is_retrieval": True})}\n\n'
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
        #获得session对应聊天记录web链接
        messages = ChatMessage.objects.filter(session=session)
        return HttpResponse(json.dumps({'session_id': str(session.session_id), 'name': session.name,
                                         'start_time': str(session.start_time), 'history': history,
                                           'books': [{'id': str(book.id), 'title': book.title} for book in books],
                                             'web_search': [{'web_search_results': message.web_search_results, 'index': message.index,
                                                              'is_retrieval': message.is_retrieval} for message in messages]
                                           }))

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