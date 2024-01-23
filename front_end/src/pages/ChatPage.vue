<script setup>
import { nextTick, ref, watch } from 'vue';
import Message from '../components/Message.vue';
import { Toaster, toast} from 'vue-sonner';
import { fetchEventSource } from '@microsoft/fetch-event-source';
//autosize
import autosize from 'autosize';
import { onMounted } from 'vue';

const welcomeMessage = { "role": "ai", "text": '你好，我是sephirah，请问有什么我可以帮忙的吗？', "end": false}
const messages = ref([welcomeMessage])
const inputText = ref('')
const sessionID = ref('')
const remainChat = ref(1)
const maxChat = ref(10)

onMounted(() => {
  autosize(document.querySelectorAll('textarea'));
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
  messages.value.push({ "role": "user", "text": inputText.value })
  const sendText = inputText.value
  const newMessage = { "role": "ai", "text": ' ' }
  messages.value.push(newMessage)
  const lastMessage = messages.value[messages.value.length - 1]
  inputText.value = ''
  //请求服务器的会话
  if (sessionID.value === '') {
    //post调用
    const response = await fetch('http://localhost:8000/api/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({
        "message": sendText
      })
    })
    const data = await response.json()
    sessionID.value = data.session_id
    console.log(sessionID.value)
  }
  await fetchEventSource('http://localhost:8000/api/chat/sse_invoke', {
    method: 'POST',
    body: JSON.stringify({
      "message": sendText,
      "session_id": sessionID.value
    }),
    onmessage(event) {
      //解析服务器返回的json数据
      const data = JSON.parse(event.data)
      lastMessage.text += data.message
      //如果是最后一条消息，就把end设置为true
      lastMessage.end = data.end
    }
  })
  //剩余聊天次数减少
  remainChat.value -= 1
}
function reset() {
  messages.value = [welcomeMessage]
  inputText.value = ''
  sessionID.value = ''
  remainChat.value = 1
  maxChat.value = 10
}

</script>

<template>
  <q-page>
    <Toaster position="top-center" />
    <message-container>
      <Message v-for="message in messages" :text="message.text" :end="message.end" :role="message.role" :remain="remainChat" :total="maxChat" />
    </message-container>
    <input-area>
      <input-container>
        <textarea autofocus v-model="inputText" type="textarea" @keydown.enter.preventDefault="sendMessage($event) " max-length="4000"
          placeholder="请输入你的问题" />
        <button class="material-icons submit-button" @click="sendMessage">send</button>
      </input-container>
      <button class="material-icons new-chat" @click="reset">restart_alt</button>
    </input-area>
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

input-area {
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
  border-radius: 0.5rem;
  border: 2px solid $border;
  outline: none;
}

input-container textarea {
  font-size: 1rem;
  line-height: 1rem;
  height: 1rem;
  resize: none;
  width: 92%;
  max-width: 92%;
  border-radius: 0.5rem;
  border: none;
  outline: none;
  background-color: transparent;
}

input-area button {
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
  border: 2px solid $border;
  border-radius: 0.5rem;
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
