<template >
  <q-item clickable :to="to" :active="active" class="q-my-sm sephirah-drawer-item"
    :active-class="'q-my-sm sephirah-drawer-item--active'">
    <q-item-section avatar>
      <q-icon :name="icon" :color="color" v-if="icon" style="font-size: 2rem" />
    </q-item-section>
    <q-item-section>
      {{ title }}
    </q-item-section>
  </q-item>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    required: false
  },
  to: {
    type: String,
    required: false
  },
  color: {
    type: String,
    required: false
  },
  active: {
    type: Boolean,
    required: false
  }
})
</script>

<style scoped lang="scss">
.sephirah-drawer-item {
  font-size: 1rem;
  height: 40px;
  border-radius: $border-radius;
}

.sephirah-drawer-item--active {
  border: 2px solid #84d8ff;
  background-color: #ddf4ff;
}
</style>