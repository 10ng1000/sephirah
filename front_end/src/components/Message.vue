<!-- 自定义用于显示弹出的message的webcomponent组件，以适配deepchat -->
<script setup>
import {ref} from 'vue';
import {toast} from "vue-sonner";
import { onMounted} from 'vue';
import { Marked } from "marked";
import { markedHighlight } from "marked-highlight";
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
//'github-markdown-css';
import 'github-markdown-css/github-markdown.css';
import { computed } from 'vue';
import { watch } from 'vue';
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
const html = ref(null);
const thumb_up = ref('thumb_up_off_alt');
const thumb_down = ref('thumb_down_off_alt');
const isThumbUpJumping = ref(false);
const isThumbDownJumping = ref(false);
const props = defineProps({
  text: String,
  end: Boolean,
  role: String
});
const isUser = computed(() => {
  return props.role === 'user';
});
onMounted(() => {
  if (props.text !== null){
    html.value = marked.parse(props.text);
  }
});
watch(() => props.text, () => {
  html.value = marked.parse(props.text);
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
  <main :class="{userMessage: isUser, aiMessage: !isUser}">
  <div v-html="html" class="markdown-body"></div>
  <div v-if="end">
  <hr/>
  <div class="buttons">
    <button :class="['material-icons',{'is-jumping': isThumbUpJumping}]" @click="changeThumbUp">{{thumb_up}}</button>
    <button :class="['material-icons',{'is-jumping': isThumbDownJumping}]" @click="changeThumbDown">{{ thumb_down }}</button>
    <button class="material-icons copy-btn" @click="copyText">content_copy</button>
  </div>
  </div>
  </main>
</template>

<style scoped lang="scss">
main{
  padding: 1rem;
  width: fit-content;
  max-width: 60%;
  border-radius: 0.5rem;
  box-shadow: 0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16);
  margin-bottom: 2rem;
}
button {
  font-size: 1.5rem;
  background-color: transparent;
  border: none;
  color: $component;
  cursor: pointer;
  outline: none;
}
hr {
  border: 0;
  height: 0.1rem;
  background: $component;
}
.userMessage {
  margin-right: 5%;
  margin-left: auto;
}
.aiMessage {
  margin-left: 5%;
  margin-right: auto;
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

