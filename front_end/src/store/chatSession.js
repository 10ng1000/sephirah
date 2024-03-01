import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatSessionStore = defineStore( 'chatSession',() =>{
    const chatSession = ref(null)
    


    return {chatSession}
})