import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRagActiveStore = defineStore( 'ragActive',() =>{
    const ragActive = ref(false)

    return {ragActive}
})