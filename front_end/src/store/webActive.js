import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useWebActiveStore = defineStore( 'webActive',() =>{
    const webActive = ref(false)

    return {webActive}
})