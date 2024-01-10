<template>
  <q-page>
    <chat-view />
  </q-page>
</template>
<script setup>
import { ref } from 'vue';
import ChatView from 'src/components/ChatView.vue';
const messages = ref([
  {role: "user", text: "hey" },
  {role: "ai", text: "hello" },
])

</script>

<style scoped lang="scss">
.q-page {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  //对齐底部
  justify-content: center;
  padding-bottom: 5%;
}
</style>

