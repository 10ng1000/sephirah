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
  <q-layout view="lHh Lpr lFf">
    <q-drawer v-model="leftDrawerOpen" show-if-above bordered :width="256" style="border-right: 1px solid gainsboro;">
      <q-list>
        <q-item header class="main-logo">Sephirah</q-item>
        <div class="col q-mx-md q-mt-md justify-start">
          <DrawerLink v-for="link in drawerLinks" :key="link.title" :title="link.title" :icon="link.icon" :to="link.to"
            :color="link.color" :active="link.active"/>
        </div>
      </q-list>
    </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style lang="scss" scoped>
.main-logo {
  color: #58cc02;
  font-family: "Alice";
  font-size: 2.5rem;
  font-weight: bold;
  justify-content: center;
}
.main-logo:hover {
  background-color: transparent;
}
</style>