<script setup>
import { computed, ref } from 'vue'
import DrawerLink from '../components/DrawerLink.vue'
import { Toaster } from 'vue-sonner'
import {useChatSessionStore} from '../store/chatSession';
import { storeToRefs } from 'pinia';

const leftDrawerOpen = ref(false)
const {chatSession} = storeToRefs(useChatSessionStore())

//todo 跳转页面
const drawerLinks = ref([
  {
    title: '记忆库',
    icon: 'memory',
    to: '/memory',
    color: 'purple'
  },
  {
    title: '知识库',
    icon: 'shelves',
    to: '/knowledge',
    color: 'blue'
  },
  {
    title: '角色',
    icon: 'settings',
    to: '/role',
    color: 'green'
  },
  // {
  //   title: '设置',
  //   icon: 'settings',
  //   to: '/settings',
  //   color: 'green'
  // }
  // {
  //   title: '提取',
  //   icon: 'sync',
  //   to: '/extract',
  //   color: 'red'
  // }
])

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

</script>

<template>
  <div class="page-wrapper">
    <nav style="border-right: 2px solid gainsboro;">
      <img src="../assets/logo.svg" alt="Description" width="100" height="100">
      <div class="link-container">
      <DrawerLink :title="'聊天'" :icon="'chat'" :to="'/chat' + (chatSession ? '/' + chatSession : '')" :color="'orange'"/>
      <DrawerLink v-for="link in drawerLinks" :title="link.title" :icon="link.icon" :to="link.to" :color="link.color"/>
      </div>
    </nav>
    <div class="main-wrapper">
      <Toaster position="top-center" richColors />
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.page-wrapper {
  height: 100vh;
  display: grid;
  grid-template-columns: 16% auto;
}
nav {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
img {
  margin-top: 2rem;
  /* color: #58cc02; */
  /* font-family: "Alice";
  font-size: 2.5rem;
  font-weight: bold; */
}
@media (max-width: 768px) {
  header {
    font-size: 0;
  }
}
.main-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: auto;
  width: 100%;
}
.link-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin-top: 2rem;
  width: 100%;
}
</style>