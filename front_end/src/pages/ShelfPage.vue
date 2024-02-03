<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { toast} from 'vue-sonner';
import axios from 'axios'
import Book from '../components/Book.vue';

const router = useRouter()
const files = ref(null)
const editFiles = ref(null)

const newTitle = computed(() => {
    if (!files.value) {
        return '上传文档'
    }
    return files.value[0].name
})

const hasFile = computed(() => {
    return files.value !== null
})

const books = ref([])

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
    axios.get('api/books/').then(
        response => {
            books.value = response.data
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
            <button class="book-button material-icons" v-if="files != null">upload_file</button>
        </form>
        </label>
        <Book class="document-container" v-for="book in books" :id="book.id" :title="book.title"/>
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
  width: 14vw;
  height: 40vh;
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
