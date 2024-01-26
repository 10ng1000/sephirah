<script setup>
import { ref } from 'vue'
import DrawerLink from '../components/DrawerLink.vue'

const leftDrawerOpen = ref(false)

const drawerLinks = ref([
  {
    title: '问答',
    icon: 'chat',
    to: '/chat',
    color: 'orange'
  },
  {
    title: '记忆库',
    icon: 'memory',
    to: '/memory',
    color: 'purple'
  },
  {
    title: '知识库',
    icon: 'book',
    to: '/knowledge',
    color: 'blue'
  },
  {
    title: '知识图谱',
    icon: 'hub',
    to: '/graph',
    color: 'green'
  },
  {
    title: '提取',
    icon: 'sync',
    to: '/extract',
    color: 'red'
  }
])

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

</script>

<template>
  <main-container>
    <nav style="border-right: 2px solid gainsboro;">
      <header>Sephirah</header>
      <link-container>
      <DrawerLink v-for="link in drawerLinks" :key="link.title" :title="link.title" :icon="link.icon" :to="link.to"
        :color="link.color" :active="link.active"/>
      </link-container>
    </nav>
    <main>
    <router-view />
    </main>
  </main-container>
</template>

<style lang="scss" scoped>
main-container {
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
header {
  margin-top: 1rem;
  color: #58cc02;
  font-family: "Alice";
  font-size: 2.5rem;
  font-weight: bold;
}
@media (max-width: 768px) {
  header {
    font-size: 0;
  }
}
main {
  display: flex;
  flex-direction: column;
  align-items: center;
}
link-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin-top: 1rem;
  width: 100%;
}
</style>