<script setup>
import { computed, ref, watch } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import Message from '../components/Message.vue';
import { Toaster, toast} from 'vue-sonner';
import { fetchEventSource } from '@microsoft/fetch-event-source';
import autosize from 'autosize';
import { onMounted } from 'vue';
import {useFloating, offset, computePosition} from '@floating-ui/vue';

const welcomeMessage = { "role": "system", "content": '你好，我是sephirah，请问有什么我可以帮忙的吗？', "end": false}
const router = useRouter()
const maxChat = 10

const messages = ref([welcomeMessage])
const inputText = ref('')
//sessionId从路由获取
const sessionId = ref('')

//展示tooltip
const showTooltip = ref(false)
const restart = ref(null)
const tooltip = ref(null)
const { floatingStyles } = useFloating(restart, tooltip, {
  placement: 'top',
  middleware: [offset(10)]
})

const remainChat = computed(() => {
  //计算所有role为assistant的message数量
  const assistantMessages = messages.value.filter(message => message.role === 'user')
  return maxChat - assistantMessages.length
})

//当剩余次数为0时，弹出提示
watch(() => remainChat.value, () => {
  if (remainChat.value === 0) {
    toast('本次记忆已用尽，请开启新的记忆', {
      type: 'negative',
      position: 'top-center',
      timeout: 3000
    })
  }
})

async function sendMessage(e) {
  if (e) {
    e.preventDefault()
  }
  messages.value.push({ "role": "user", "content": inputText.value })
  const sendText = inputText.value
  const newMessage = { "role": "assistant", "content": ' ' }
  messages.value.push(newMessage)
  const lastMessage = messages.value[messages.value.length - 1]
  inputText.value = ''
  //请求服务器的会话
  if (sessionId.value === '') {
    //post调用
    const response = await fetch(import.meta.env.VITE_BACKEND_URL + '/api/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({
        "message": sendText
      })
    })
    const data = await response.json()
    sessionId.value = data.session_id
    router.replace({path: `/chat/${sessionId.value}`})
  }
  await fetchEventSource(import.meta.env.VITE_BACKEND_URL + '/api/chat/sse_invoke', {
    method: 'POST',
    body: JSON.stringify({
      "message": sendText,
      "session_id": sessionId.value
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
  sessionId.value = ''
  router.replace({path: "/chat"})
}

onMounted(() => {
  autosize(document.querySelectorAll('textarea'));
  const route = useRoute()
  if (route.params.session_id) {
    sessionId.value = route.params.session_id
    //加载历史消息
    fetch(`http://localhost:8000/api/chat/sessions?session_id=${sessionId.value}`)
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
  <q-page>
    <Toaster position="top-center" />
    <message-container>
      <Message v-for="message in messages" :content="message.content" :end="message.end" :role="message.role" :remain="remainChat" :total="maxChat" />
    </message-container>
    <footer>
      <input-container>
        <textarea autofocus v-model="inputText" type="textarea" @keydown.enter.preventDefault="sendMessage($event) " max-length="4000"
          placeholder="请输入你的问题" />
        <button class="material-icons submit-button" @click="sendMessage">send</button>
      </input-container>
      <button ref="restart" class="material-icons new-chat" @click="reset" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">restart_alt</button>
      <div class="tooltip" ref="tooltip" :style="floatingStyles" v-if="showTooltip">开启新记忆</div>
    </footer>
  </q-page>
</template>

<style scoped lang="scss">
message-container {
  width: 65%;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: auto;
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

input-container {
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
  border-radius: $border-radius;
  border: $border;
  outline: none;
}

input-container textarea {
  line-height: 1rem;
  height: 1rem;
  resize: none;
  width: 92%;
  max-width: 92%;
  border-radius: $border-radius;
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
  color: $component;
}

.new-chat {
  margin-left: 1rem;
  height: 3rem;
  border: $border;
  border-radius: $border-radius-small;
  color: pink;
  font-size: 2rem;
}

.new-chat:hover {
  background-color: #f5f5f5;
}

.q-page {
  display: flex;
  flex-direction: column;
  //对齐底部
  justify-content: flex-start;
  align-items: center;
}
</style>
