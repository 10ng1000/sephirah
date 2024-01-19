from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.http import StreamingHttpResponse
from utils.zhipu_llm import ZhipuLLM
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