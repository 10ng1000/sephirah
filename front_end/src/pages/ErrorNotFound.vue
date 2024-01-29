<template>
  <main>
  <div style="font-size: 30vh">
        404
  </div>
  <div style="font-size: 10vh; max-width: 80%">
        你似乎进入了未被开发的领域
  </div>
  </main>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ErrorNotFound'
})
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
