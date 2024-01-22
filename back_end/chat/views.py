from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from utils.zhipu_llm import ZhipuLLM
from utils.chat_with_memory import chat_sse
from chat.models import ChatSession
import json

# Create your views here.
class ChatSseView(View):
    zhipuLLM = ZhipuLLM()
    def post(self, request):
        data = json.loads(request.body)
        message = data.get('message')
        #print(f'message: {message}')
        def event_stream():
            for chunk in self.zhipuLLM.stream(message):
                yield f'data: {json.dumps({"message" : chunk, "end": False})}\n\n'
            yield f'data: {json.dumps({"message" : "", "end": True})}\n\n'
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

class ChatView(View):
    zhipuLLM = ZhipuLLM()
    def post(self, request):
        '''messge是用户输入传给大模型的文本'''
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