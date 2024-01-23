from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from utils.zhipu_llm import ZhipuLLMWithMemory
from chat.models import ChatSession
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

class ChatView(View):
    def post(self, request):
        '''暂时弃用'''
        data = json.loads(request.body)
        message = data.get('message')
        return HttpResponse(json.dumps({'text': self.zhipuLLM().invoke(message)}))

class ChatSessionView(View):
    def post(self, request):
        # 创建一个新的大模型对话session
        # 使用时间戳加随机数作为session_id
        import time
        import secrets
        session_id = f'{int(time.time())}-{secrets.token_hex(8)}'
        #把id存入数据库
        session = ChatSession(session_id=session_id)
        session.save()
        return HttpResponse(json.dumps({'session_id': session_id}))
    
    def get(self, request):
        # 获取所有大模型对话session
        sessions = ChatSession.objects.all()
        return HttpResponse(json.dumps({'sessions': [session.session_id for session in sessions]}))