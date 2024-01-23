<script setup>
import { ref } from 'vue';
import Message from '../components/Message.vue';
import { Toaster } from 'vue-sonner';
import {fetchEventSource} from '@microsoft/fetch-event-source';
//autosize
import autosize from 'autosize';
import { onMounted } from 'vue';


const messages = ref([
  { "role": "ai" , "text": '你好，我是sephirah，请问有什么我可以帮忙的吗？'}
])
const inputText = ref('')
const sessionID = ref('')


onMounted(() => {
  autosize(document.querySelectorAll('textarea'));
})

async function sendMessage(e) {
  if (e) {
    e.preventDefault()
  }
  messages.value.push({"role": "user", "text": inputText.value})
  const sendText = inputText.value
  const newMessage = {"role": "ai", "text": ' '}
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
  await fetchEventSource ('http://localhost:8000/api/chat/sse_invoke', {
    method: 'POST',
    body: JSON.stringify({
      "message": sendText,
      "session_id": sessionID.value
    }),
    onmessage(event) {
      //解析服务器返回的json数据
      const data = JSON.parse(event.data)
      lastMessage.text += data.message
      //滚动到最底部
      const messageContainer = document.querySelector('.message-container')
      messageContainer.scrollTop = messageContainer.scrollHeight
    }
  })
}

</script>

<template>
  <q-page>
    <Toaster position="top-center"/>
    <div class="message-container">
      <Message v-for="message in messages" :text="message.text" :end="true" :role="message.role"/>
    </div>
    <div class="input-container">
    <textarea v-model="inputText" type="textarea" @keydown.enter.preventDefault="sendMessage($event)" placeholder="请输入你的问题" />
    <button class="material-icons" @click="sendMessage">send</button>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
.message-container {
  width: 65%;
  padding-top: 5vh;
  margin-top: 0;
  margin-bottom: auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: auto;
}
.input-container {
  min-height: 7vh;
  width: 65%;
  padding-inline: 1rem;
  margin-top: auto;
  margin-bottom: 5vh;
  display: flex;
  flex-direction: row;
  justify-content:flex-start;
  align-items: center;
  border-radius: 0.5rem;
  border: 1px solid #ccc;
  outline: none;
}
.input-container textarea {
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
.input-container button{
  margin-left: auto;
  font-size: 1.5rem;
  border: none;
  outline: none;
  background-color: transparent;
  cursor: pointer;
  color: $component;
}

.q-page {
  display: flex;
  flex-direction: column;
  //对齐底部
  justify-content: flex-start;
  align-items: center;
}
</style>
