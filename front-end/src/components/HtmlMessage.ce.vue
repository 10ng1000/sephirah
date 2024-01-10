<!-- 自定义用于显示弹出的message的webcomponent组件，以适配deepchat -->
<script setup>
import {ref} from 'vue';
import { matThumbUpOffAlt } from '@quasar/extras/material-icons'
const test = ref(true);



</script>
<template>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
      rel="stylesheet">
  <div v-if="test">
  <slot></slot>
  </div>
  <button class="material-icons" @click="test = !test">thumb_up_off_alt</button>
</template>

<style scoped>
button {
  background-color: transparent;
  border: none;
  color: #2870EA;
  font-size: 20px;
  cursor: pointer;
  outline: none;
}
</style>
