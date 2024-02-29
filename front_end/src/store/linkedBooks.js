import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLinkedBooksStore = defineStore( 'linkedBooks',() =>{
    const linkedBooks = ref([])

    return {linkedBooks}
})