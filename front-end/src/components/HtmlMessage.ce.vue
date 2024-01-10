<!-- 自定义用于显示弹出的message的webcomponent组件，以适配deepchat -->
<script setup>
import {ref} from 'vue';
import { onMounted } from 'vue';
import {toast} from "vue-sonner";
const thumb_up = ref('thumb_up_off_alt');
const thumb_down = ref('thumb_down_off_alt');
const isThumbUpJumping = ref(false);
const isThumbDownJumping = ref(false);
const props = defineProps({
  text: {
    type: String
  }
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
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
        rel="stylesheet">
  <div>
    <p v-if="props.text">{{ props.text }}</p>
  </div>
  <hr/>
  <div class="buttons">
    <!-- 按钮点击后填充颜色 -->
    <button :class="['material-icons',{'is-jumping': isThumbUpJumping}]" @click="changeThumbUp">{{thumb_up}}</button>
    <button :class="['material-icons',{'is-jumping': isThumbDownJumping}]" @click="changeThumbDown">{{ thumb_down }}</button>
    <button class="material-icons copy-btn" @click="copyText">content_copy</button>
  </div>
</template>

<style scoped>
p {
  margin-top: 0.2rem;
  margin-bottom: 0.2rem;
}
button {
  background-color: transparent;
  border: none;
  color: #2870EA;
  cursor: pointer;
  outline: none;
}
hr {
  border: 0;
  height: 0.1rem;
  background: #2870EA;
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
