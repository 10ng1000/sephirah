<script setup>
import { ref, computed} from 'vue'
const props = defineProps({
  title: String,
  icon: String,
  to: String,
  color: String,
  active: 
    {
        type: Boolean,
        default: false
    }
})

const activeClass = computed(() => {
  return props.active ? 'sephirah-drawer-item--active' : ''
})
</script>

<template >
    <router-link :to="props.to" activeClass="sephirah-drawer-item--active">
        <link-icon class="material-icons" :style="{color:props.color}">{{ props.icon }}</link-icon>
        <link-title>{{ props.title }}</link-title>
    </router-link>
</template>
  

<style scoped lang="scss">

  
.sephirah-drawer-item--active {
    border: 2px solid #84d8ff;
    background-color: #ddf4ff;
}
  
a {
  margin-top: 0.5rem;
  border: 2px solid transparent;
  padding-left: 1rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  width: 90%;
}

link-icon {
  font-size: 2rem;
}
link-title {
  margin-left: 1.5rem;
  font-size: 1rem;
  line-height: 1rem;
}

@media (max-width: 768px) {
    link-title {
        font-size: 0;
    }
    a {
        padding-left: 0.5rem;
    }
}
</style>