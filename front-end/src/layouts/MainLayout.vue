<template>
  <q-layout view="lHh Lpr lFf">
    <q-drawer v-model="leftDrawerOpen" show-if-above bordered :width="256">
      <q-list>
        <q-item header class="main-logo row justify-center">Sephirah</q-item>
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

<script setup>
import { ref } from 'vue'
import DrawerLink from 'src/components/DrawerLink.vue'

const leftDrawerOpen = ref(false)

const drawerLinks = ref([
  {
    title: '问答',
    icon: 'chat',
    to: '/chat',
    color: 'orange'
  },
  {
    title: '知识图谱',
    icon: 'hub',
    to: '/graph',
    color: 'green'
  },
  {
    title: '知识库',
    icon: 'book',
    to: '/knowledge',
    color: 'blue'
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
