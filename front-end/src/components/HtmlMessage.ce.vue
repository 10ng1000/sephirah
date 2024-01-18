<!-- 自定义用于显示弹出的message的webcomponent组件，以适配deepchat -->
<script setup>
import {ref} from 'vue';
import {toast} from "vue-sonner";
import { onMounted, nextTick} from 'vue';
import { Marked } from "marked";
import { markedHighlight } from "marked-highlight";
import hljs from 'highlight.js';
//导入quasar项目的app
const marked = new Marked(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang, info) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext';
      return hljs.highlight(code, { language }).value;
    }
  })
);
const htmlMessage = ref(null);
const thumb_up = ref('thumb_up_off_alt');
const thumb_down = ref('thumb_down_off_alt');
const isThumbUpJumping = ref(false);
const isThumbDownJumping = ref(false);
const props = defineProps({
  text: String
});
const html = ref('');
const markdownContainer = ref(null);
onMounted(() => {
  html.value = marked.parse(props.text);
  //滚动到底部
  nextTick(() => {
    markdownContainer.value.scrollTop = markdownContainer.value.scrollHeight;
  });
});
function copyText() {
  navigator.clipboard.writeText(props.text);
  toast('已成功复制到剪贴板');
}
function changeThumbUp(){
  if (thumb_up.value === 'thumb_up_off_alt') {
    thumb_up.value = 'thumb_up';
    thumb_down.value = 'thumb_down_off_alt';
    isThumbUpJumping.value = true;
    setTimeout(() => {
      isThumbUpJumping.value = false;
    }, 300);
  } else {
    thumb_up.value = 'thumb_up_off_alt';
  }
}
function changeThumbDown(){
  if (thumb_down.value === 'thumb_down_off_alt') {
    thumb_down.value = 'thumb_down';
    thumb_up.value = 'thumb_up_off_alt';
    isThumbDownJumping.value = true;
    setTimeout(() => {
      isThumbDownJumping.value = false;
    }, 300);
  } else {
    thumb_down.value = 'thumb_down_off_alt';
  }
}
</script>

<template>
  <body ref="htmlMessage">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
        rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
  <div v-html="html" ref="markdownContainer"></div>
  <hr/>
  <div class="buttons">
    <button :class="['material-icons',{'is-jumping': isThumbUpJumping}]" @click="changeThumbUp">{{thumb_up}}</button>
    <button :class="['material-icons',{'is-jumping': isThumbDownJumping}]" @click="changeThumbDown">{{ thumb_down }}</button>
    <button class="material-icons copy-btn" @click="copyText">content_copy</button>
  </div>
</body>
</template>

<style scoped>
body {
  font-size : 1rem;
  overflow: auto;
}
button {
  background-color: transparent;
  border: none;
  color: #1cb0f6;
  cursor: pointer;
  outline: none;
}
hr {
  border: 0;
  height: 0.1rem;
  background: #1cb0f6;
}
.buttons {
  display: flex;
  justify-content:flex-end;
  margin-top: 0.5rem;
}
.is-jumping {
  animation: jumpAnimation 0.3s;
}
.copy-btn {
  margin-left: auto;
}
@keyframes jumpAnimation {
  0% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-0.3rem) scale(1.1);
  }
  100% {
    transform: translateY(0) scale(1);
  }
}
</style>
