<script setup>
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import axios from 'axios'
import { onMounted } from 'vue'

const inputText = ref('')
const currentSetting = ref('')

function sendSetting(e) {
  if (e) {
    e.preventDefault()
  }
  if (inputText.value === '') {
    return
  }
  let url = import.meta.env.VITE_BACKEND_URL + '/api/chat/role'
  axios.post(url, {
    setting: inputText.value
  }).then(response => {
    fetchSetting()
    toast.success('设置成功')
  }).catch(error => {
    console.log(error)
  })
}

function fetchSetting() {
  let url = import.meta.env.VITE_BACKEND_URL + '/api/chat/role'
  axios.get(url).then(response => {
    if (response.data.setting == null) {
      currentSetting.value = '目前为默认设置'
      return
    }
    currentSetting.value = response.data.setting
  }).catch(error => {
    console.log(error)
  })
}

function cancel() {
  let url = import.meta.env.VITE_BACKEND_URL + '/api/chat/role'
  axios.delete(url).then(response => {
    fetchSetting()
    toast.success('重置成功')
  }).catch(error => {
    console.log(error)
  })
}

onMounted(() => {
  fetchSetting()
})


</script>

<template>
  <main>
    <caption>当前设置</caption>
    <section>
      <span>{{ currentSetting }}</span>
    </section>
    <caption>修改设置</caption>
    <div class="input-container">
      <textarea autofocus v-model="inputText" type="textarea" @keydown.enter.prevent="sendSetting($event)"
        max-length="4000" placeholder="输入设置" />
      <button class="material-icons submit-button" @click="sendSetting">send</button>
    </div>
    <caption>重置</caption>
    <a @click="cancel" href='#/role'>点击重置</a>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  margin-bottom: 3vh;
  width: var(--main-width);
  height: 100%;
}

caption{
  align-self: flex-start;
  font-family: Alice;
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem auto 0 0;
}

section {
  border: var(--border);
  border-radius: var(--border-radius);
  width: 80%;
}

.input-container, section, a{
  margin-top: 4vh;
  margin-bottom: 2vh;
  min-height: 8vh;
  width: 60%;
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

.submit-button {
  margin-left: auto;
  border: none;
  outline: none;
  background-color: transparent;
  color: var(--component);
  font-size: 1.5rem;
}
</style>