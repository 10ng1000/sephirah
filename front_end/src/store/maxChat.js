import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMaxChatStore = defineStore( 'maxChat',() =>{
    const maxChat = ref(30)

    return {maxChat}
})