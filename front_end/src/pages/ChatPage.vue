<script setup>
import { computed, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Message from '../components/Message.vue';
import {toast } from 'vue-sonner';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import autosize from 'autosize';
import { onMounted } from 'vue';
import { offset, computePosition, autoPlacement } from '@floating-ui/vue';
import { useMaxChatStore } from '../store/maxChat';
import { useChatSessionStore } from '../store/chatSession';
import { useLinkedBooksStore } from '../store/linkedBooks';
import { useRagActiveStore } from '../store/ragActive';
import { useWebActiveStore } from '../store/webActive';
import { storeToRefs } from 'pinia';

const welcomeMessage = { "role": "system", "content": '你好，我是sephirah，请问有什么我可以帮忙的吗？', "end": false, "info":null}
const router = useRouter()
const { maxChat } = storeToRefs(useMaxChatStore())
const { chatSession } = storeToRefs(useChatSessionStore())
const { linkedBooks } = storeToRefs(useLinkedBooksStore())
const { ragActive } = storeToRefs(useRagActiveStore())
const { webActive } = storeToRefs(useWebActiveStore())

const messages = ref([welcomeMessage])
const inputText = ref('')

const showTooltip = ref(false)
const showTooltipRag = ref(false)
const showTooltipWeb = ref(false)

const usedChat = computed(() => {
  //计算所有role为assistant的message数量
  return messages.value.filter(message => message.role === 'user').length
})

const canChat = computed(() => {
  return maxChat.value - usedChat.value >= 0
})

//当剩余次数为0时，弹出提示
watch(() => usedChat.value, () => {
  if (usedChat.value === maxChat.value) {
    toast.warning('本次记忆已用尽，请开启新的记忆', {
      type: 'negative',
      position: 'top-center',
      timeout: 3000
    })
    //禁用输入框
    inputText.value = ''
  }
})

async function sendMessage(e) {
  if (e) {
    e.preventDefault()
  }
  if (inputText.value === '') {
    return
  }
  let url = import.meta.env.VITE_BACKEND_URL + '/api/chat/sse_invoke'
  if (ragActive.value) {
    if (linkedBooks.value.length === 0) {
      toast.error('文档问答模式已开启，请选择文档或者关闭文档问答模式')
      return
    }
    url = import.meta.env.VITE_BACKEND_URL + '/api/chat/sse_invoke/rag'
  }
  else if (webActive.value) {
    url = import.meta.env.VITE_BACKEND_URL + '/api/chat/sse_invoke/web_search'
  }
  messages.value.push({ "role": "user", "content": inputText.value, "info":null })
  const sendText = inputText.value
  let newMessage = { "role": "assistant", "content": ' ', "end": false, "info":null, "isRetrieval": false}
  messages.value.push(newMessage)
  let lastMessage = messages.value[messages.value.length - 1]
  inputText.value = ''
  //请求服务器的会话
  if (chatSession.value === null) {
    //post调用
    const response = await fetch(import.meta.env.VITE_BACKEND_URL + '/api/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({
        "message": sendText,
        "linked_books": linkedBooks.value
      })
    })
    const data = await response.json()
    chatSession.value = data.session_id
    router.replace({ path: `/chat/${chatSession.value}` })
  }
  await fetchEventSource(url, {
    method: 'POST',
    body: JSON.stringify({
      "message": sendText,
      "session_id": chatSession.value,
      "k": 3,
      "index": messages.value.length - 2
    }),
    onmessage(event) {
      const data = JSON.parse(event.data)
      if (data.end) {
        lastMessage.end = true
        lastMessage.info = data.message
        lastMessage.isRetrieval = data.is_retrieval
      }
      else lastMessage.content += data.message
    }
  })
}
function reset() {
  messages.value = [welcomeMessage]
  inputText.value = ''
  chatSession.value = ''
  chatSession.value = null
  router.replace({ path: "/chat" })
}
function changeRagMode() {
  //切换RAG模式
  ragActive.value = !ragActive.value
  if (ragActive.value) {
    toast.success('已切换至文档问答模式')
    webActive.value = false
  }
}

function changeWebMode() {
  webActive.value = !webActive.value
  if (webActive.value) {
    toast.success('已切换至网页搜索模式')
    ragActive.value = false
  }
}

onMounted(() => {
  autosize(document.querySelectorAll('textarea'));
  const route = useRoute()
  if (route.params.session_id) {
    chatSession.value = route.params.session_id
    //加载历史消息
    fetch(import.meta.env.VITE_BACKEND_URL + `/api/chat/sessions/${chatSession.value}`)
      .then(response => response.json())
      .then(data => {
        messages.value = [welcomeMessage]
        for (let i = 0; i < data.history.length; i++) {
          //加上end标记
          let message = { "role": "assistant", "content": ' ', "end": false, "info":null}
          message.content = data.history[i].content
          message.role = data.history[i].role
          message.end = true
          for (const web_search of data.web_search) {
            if (web_search.index == i) {
              message.info = web_search.web_search_results
              message.isRetrieval = web_search.is_retrieval
            }
          }
          messages.value.push(message)
        }
      })
    //将页面滚动到底部
    const main = document.querySelector('main')
    main.scrollTop = main.scrollHeight
  }

  //计算tooltip位置
  const rag = document.querySelector('.rag-btn')
  const ragtooltip = document.querySelector('#ragtooltip')
  const restart = document.querySelector('.new-chat')
  const refreshtooltip = document.querySelector('#refreshtooltip')
  computePosition(restart, refreshtooltip, {
    placement: 'top',
    middleware: [offset({
      mainAxis: 50,
      crossAxis: -50
    })]
  }).then(({ x, y }) => {
    Object.assign(refreshtooltip.style, {
      left: `${x}px`,
      top: `${y}px`,
    });
  });

  computePosition(rag, ragtooltip, {
    placement: 'top',
    middleware: [offset({
      mainAxis: 50,
      crossAxis: -60
    })]
  }).then(({ x, y }) => {
    Object.assign(ragtooltip.style, {
      left: `${x}px`,
      top: `${y}px`,
    });
  });

  const web = document.querySelector('.web-btn')
  computePosition(web, webtooltip, {
    placement: 'top',
    middleware: [offset({
      mainAxis: 50,
      crossAxis: -60
    })]
  }).then(({ x, y }) => {
    Object.assign(webtooltip.style, {
      left: `${x}px`,
      top: `${y}px`,
    });
  });
})
</script>

<template>
  <main>
    <div class="message-wrapper">
      <Message v-for="(message, index) in messages" :content="message.content" :end="message.end" :role="message.role"
        :info="message.info" :isretrieval="message.isRetrieval" :remain="index / 2" :total="maxChat" />
    </div>
  </main>
  <footer>
    <div class="input-container">
      <textarea autofocus v-model="inputText" type="textarea" @keydown.enter.prevent="sendMessage($event)"
        max-length="4000" placeholder="请输入你的问题" :disabled="!canChat" />
      <button class="material-icons submit-button" @click="sendMessage" :disabled="!canChat">send</button>
    </div>
    <button ref="restart" class="material-icons new-chat" @click="reset" @mouseenter="showTooltip = true"
      @mouseleave="showTooltip = false">restart_alt</button>
    <button ref="rag" class="material-icons rag-btn" :class="{ 'rag-active': ragActive }" @click="changeRagMode"
      @mouseenter="showTooltipRag = true" @mouseleave="showTooltipRag = false">book</button>
    <button ref="web" class="material-icons web-btn" :class="{ 'web-active': webActive }" @click="changeWebMode"
      @mouseenter="showTooltipWeb = true" @mouseleave="showTooltipWeb = false">language</button>
  </footer>
  <div id="ragtooltip" ref="ragtooltip" class="tooltip" v-show="showTooltipRag">文档问答模式</div>
  <div id="refreshtooltip" ref="refreshtooltip" class="tooltip" v-show="showTooltip">开启新记忆</div>
  <div id="webtooltip" ref="webtooltip" class="tooltip" v-show="showTooltipWeb">网页搜索模式</div>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: auto;
  width: 100%;
}

.message-wrapper {
  width: 65%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-self: center;
}

footer {
  width: 100%;
  position: sticky;
  bottom: 0;
  margin-top: auto;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: white;
}

.input-container {
  margin-top: 2vh;
  margin-bottom: 2vh;
  align-self: center;
  min-height: 7vh;
  width: 65%;
  padding-inline: 1rem;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  border-radius: var(--border-radius);
  border: var(--border);
  outline: none;
}

textarea {
  line-height: 1rem;
  height: 1rem;
  font-size: 1rem;
  resize: none;
  width: 92%;
  max-width: 92%;
  border-radius: var(--border-radius);
  border: none;
  outline: none;
  background-color: transparent;
}

footer button {
  cursor: pointer;
  color: var(--component);
  margin-left: 1rem;
  height: 3rem;
  border: var(--border);
  border-radius: var(--border-radius-small);
  font-size: 2rem;
}

.submit-button {
  margin-left: auto;
  border: none;
  outline: none;
  background-color: transparent;
  color: var(--component);
  font-size: 1.5rem;
}

.submit-button:hover {
  background-color: transparent;
}

.new-chat {
  color: pink;
}

.rag-btn, .web-btn {
  color: grey;
}

.rag-active {
  color: green;
}

.web-active {
  color: blue;
}

footer button:hover {
  background-color: #f5f5f5;
}
</style>
