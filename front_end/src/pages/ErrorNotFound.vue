<template>
  <main>
  <div style="font-size: 30vh">
        404
  </div>
  <div style="font-size: 10vh; max-width: 80%">
        你似乎输入了一个错误的网址，
        或者该网址正在维护中
  </div>
  </main>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ErrorNotFound'
})
</script>

<style lang="scss" scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
