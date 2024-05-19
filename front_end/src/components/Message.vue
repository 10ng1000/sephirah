<!-- 自定义用于显示弹出的message的webcomponent组件，以适配deepchat -->
<script setup>
import { ref } from 'vue';
import { toast } from "vue-sonner";
import { onMounted } from 'vue';
import { Marked } from "marked";
import { markedHighlight } from "marked-highlight";
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
//'github-markdown-css';
import 'github-markdown-css/github-markdown.css';
import copy from 'copy-to-clipboard';
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
const isScrolling = ref(false);
const showInfo = ref(false);

const props = defineProps({
  content: String,
  end: Boolean,
  role: String,
  remain: Number,
  total: Number,
  info: String,
  isretrieval: Boolean
});

const isUser = computed(() => {
  return props.role === 'user';
});

const searchInfo = computed(() => {
  if(props.info==null || props.info=='')
    return null
  else{
    const newStr = props.info.replace(/'/g, '"');
    const obj = JSON.parse(newStr);
    return obj
  }
});

const showInfoMessage = computed(() => {
  return showInfo.value ? '隐藏来源' : '显示来源';
});

onMounted(() => {
  if (props.content !== null) {
    html.value = marked.parse(props.content);
  }
  window.addEventListener('scroll', function (event) {
    isScrolling.value = true;
  }, true);
});
watch(() => props.content, () => {
  html.value = marked.parse(props.content);
  //视图更新后，滚动到底部，但是两次滚动之间要有间隔，滚动动画要平滑,如果用户滚动了，就不要滚动到底部了
  if (!isScrolling.value) {
    setTimeout(() => {
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
      });
    }, 100);
  }
});
function copyText() {
    copy(props.content);
    toast.success('已成功复制到剪贴板');
}
function changeThumbUp() {
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
function changeThumbDown() {
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
  <article :class="['message-container' ,{userMessage: isUser, aiMessage: !isUser}]">
    <div v-html="html" class="markdown-body"></div>
    <a v-show="searchInfo!=null" @click="showInfo = !showInfo" href="#">{{ showInfoMessage }}</a>
    <a v-show="showInfo && !isretrieval" v-for="item in searchInfo" :href="item.link" target="_blank">{{`[${item.media}]   ${item.title}`}}</a>
    <div class="cite" v-show="showInfo && isretrieval" v-for="item in searchInfo">{{`[${item.media}]   ${item.title}`}}</div>
    <div v-if="!isUser">
      <hr />
      <div class="button-container">
        <button :class="['material-icons', { 'is-jumping': isThumbUpJumping }]" @click="changeThumbUp">{{ thumb_up }}</button>
        <button :class="['material-icons', { 'is-jumping': isThumbDownJumping }]" @click="changeThumbDown">{{ thumb_down
        }}</button>
        <button :class="['material-icons', {'copy-btn': !end}]" @click="copyText">content_copy</button>
        <span class="remain-text" v-if="end">
          {{ remain }}/{{ total }}
        </span>
      </div>
    </div>
  </article>
</template>

<style scoped>

.cite{
  margin-top: 0.5rem;
  font-family: Alice;
}

a {
  color: var(--component);
  text-decoration: none;
  cursor: pointer;
}

.message-container {
  margin-top: 2rem;
  border: var(--border);
  border-radius: var(--border-radius);
  max-width: 80%;
  padding: 1rem;
}

button {
  font-size: 1.5rem;
  background-color: transparent;
  border: none;
  color: var(--component);
  cursor: pointer;
  outline: none;
}

hr {
  border: 0;
  height: 0.1rem;
  background: var(--component);
}

.remain-text {
  margin-left: auto;
  line-height: 1.5rem;
  font-size: 1.2rem;
  align-self:flex-end;
}


.userMessage {
  margin-right: 5%;
  margin-left: auto;
}

.aiMessage {
  margin-left: 5%;
  margin-right: auto;
}

.button-container {
  display: flex;
  justify-content: flex-start;
  margin-top: 0.5rem;
}

.is-jumping {
  animation: jumpAnimation 0.3s;
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
}</style>

