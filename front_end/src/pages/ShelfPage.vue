<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import axios from 'axios'
import Book from '../components/Book.vue';
import {useChatSessionStore} from '../store/chatSession';
import { storeToRefs } from 'pinia';

const files = ref(null)
const books = ref([])
const store = useChatSessionStore()
const {chatSession} = storeToRefs(store)

const newTitle = computed(() => {
    if (!files.value) {
        return '上传文档'
    }
    return files.value[0].name
})


function handleFileChange() {
    const input = document.getElementById('file-input')
    files.value = input.files
}


async function handleSubmit(){
    const formData = new FormData()
    formData.append("file", files.value[0])
    axios.post('api/books/',formData).then(
        () => {
            fetchBooks()
            files.value = null
        }
    )
}

async function fetchBooks(){
    let linkedBooks = []
    if (chatSession.value) {
        axios.get(`api/chat/sessions/${chatSession.value}/books`).then(
            response => {
                response.data.forEach(book => {
                    linkedBooks.push(book.id)
                    console.log(book.id)
                })
            }
        )
    }
    axios.get('api/books/').then(
        response => {
            books.value = response.data
            // 用linkedBooks更新books的isLinked属性
            books.value.forEach(book => {
                book.isLinked = linkedBooks.includes(book.id)
                console.log(book.isLinked)
            })

        }
    )
}

onMounted( async ()=>{
    await fetchBooks()
})

</script>

<template>
    <input type="file" id="file-input" accept=".txt" @change="handleFileChange"/>
    <main>
        <label for="file-input" class="document-container add-document">
        <form method="post" action enctype="multipart/form-data" @submit.prevent="handleSubmit">
            <div v-show="files === null">+</div>
            <!-- todo 加上颜色前后变换 -->
            <div>{{newTitle}}</div>
            <!-- todo 激活的放在前面 -->
            <button class="book-button material-icons" v-if="files != null">upload_file</button>
        </form>
        </label>
        <Book class="document-container" v-for="book in books" :id="book.id" :title="book.title" :isLinked="book.isLinked"/>
    </main>
</template>

<style scoped>
main {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: auto;
    justify-content: center;
    align-items: center;
    gap: 2rem 2rem;
    width: 80%;
    height: 80%;
    font-family: Alice;
    text-align: center;
}

.document-container {
  width: 12rem;
  height: 17rem;
}

.add-document {
  margin: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  font-size: 2rem;
  border: 2px dashed hsl(92, 59%, 66%);
  border-radius: var(--border-radius-small);
  padding: 2rem;
  color: var(--component);
  box-shadow: none;
  cursor: pointer;
}

.document-container:hover {
  border-color: var(--book-color);
}

@media (max-width: 768px) {
    main {
        display: flex;
        flex-direction: column;
        justify-content: start;
        gap: 0;
        margin-top: 5vh;
    }
    .document-container {
        flex-shrink: 0;
        width: 30vw;
        height: 25vh;
        margin-top: 5vh;
    }
}

</style>
