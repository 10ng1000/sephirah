<script setup>
import { computed, ref, watch } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import Message from '../components/Message.vue';
import { Toaster, toast} from 'vue-sonner';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import autosize from 'autosize';
import { onMounted } from 'vue';
import {useFloating, offset, computePosition} from '@floating-ui/vue';
import {useMaxChatStore} from '../store/maxChat';
import {useChatSessionStore} from '../store/chatSession';
import { useLinkedBooksStore } from '../store/linkedBooks';
import { storeToRefs } from 'pinia';

const welcomeMessage = { "role": "system", "content": '你好，我是sephirah，请问有什么我可以帮忙的吗？', "end": false}
const router = useRouter()
const {maxChat} = storeToRefs(useMaxChatStore() )
const {chatSession} = storeToRefs(useChatSessionStore())
const {linkedBooks} = storeToRefs(useLinkedBooksStore())

const messages = ref([welcomeMessage])
const inputText = ref('')

//展示tooltip
const showTooltip = ref(false)
const restart = ref(null)
const tooltip = ref(null)
const { floatingStyles } = useFloating(restart, tooltip, {
  placement: 'top',
  middleware: [offset(10)]
})

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
  messages.value.push({ "role": "user", "content": inputText.value })
  const sendText = inputText.value
  const newMessage = { "role": "assistant", "content": ' ' }
  messages.value.push(newMessage)
  const lastMessage = messages.value[messages.value.length - 1]
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
    router.replace({path: `/chat/${chatSession.value}`})
  }
  await fetchEventSource(import.meta.env.VITE_BACKEND_URL + '/api/chat/sse_invoke', {
    method: 'POST',
    body: JSON.stringify({
      "message": sendText,
      "session_id": chatSession.value,
    }),
    onmessage(event) {
      const data = JSON.parse(event.data)
      lastMessage.content += data.message
      lastMessage.end = data.end
    }
  })
}
function reset() {
  messages.value = [welcomeMessage]
  inputText.value = ''
  chatSession.value = ''
  router.replace({path: "/chat"})
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
        for (const message of data.history) {
          //加上end标记
          message.end = true
          messages.value.push(message)
        }
      })
  }
})

</script>

<template>
    <main>
      <div class="message-wrapper">
      <Message v-for="(message, index) in messages" :content="message.content" :end="message.end" :role="message.role" :remain="index / 2" :total="maxChat" />
      </div>
    </main>
    <footer>
      <div class="input-container">
        <textarea autofocus v-model="inputText" type="textarea" @keydown.enter.prevent="sendMessage($event) " max-length="4000"
          placeholder="请输入你的问题" :disabled="!canChat"/>
        <button class="material-icons submit-button" @click="sendMessage" :disabled="!canChat">send</button>
      </div>
      <button ref="restart" class="material-icons new-chat" @click="reset" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">restart_alt</button>
      <div class="tooltip" ref="tooltip" :style="floatingStyles" v-if="showTooltip">开启新记忆</div>
    </footer>
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
  margin-left: auto;
  font-size: 1.5rem;
  border: none;
  outline: none;
  background-color: transparent;
  cursor: pointer;
  color: var(--component);
}

.new-chat {
  margin-left: 1rem;
  height: 3rem;
  border: var(--border);
  border-radius: var(--border-radius-small);
  color: pink;
  font-size: 2rem;
}

.new-chat:hover {
  background-color: #f5f5f5;
}
</style>
