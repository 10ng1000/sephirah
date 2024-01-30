<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { toast} from 'vue-sonner';
import axios from 'axios'

const router = useRouter()

const files = ref(null)

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

async function handleSubmit(e){
    const formData = new FormData()
    formData.append("file", files.value[0])
    //发送表单信息
    axios.post('api/books/',formData).then(
        () => {
            fetchBooksAndPush()
            files.value = null
        }
    )
}

async function fetchBooksAndPush() {
    axios.get(`api/books/`).then(
        response => {
            books.value = []
            for (const book of response.data) {
                book.isHover = 0
                books.value.unshift(book)
            }
        }
    )
}

function viewBook(bookId) {
    //跳转路由
    router.push(`/books/${bookId}`)
}

function deleteBook(bookId) {
    toast.error('确定删除该文档吗？', {
        action: {
            label: '确定',
            onClick: async () => {
                axios.delete(`api/books/${String(bookId)}`).then(
                    response => {
                        if (response.status != 204) {
                            toast.success("删除成功")
                            fetchBooksAndPush()
                        }
                        else toast.success("要删除的资源不存在")
                    }
                ).catch(
                    error => toast.error("删除失败")
                )
            }
        },
    })

}

function editBook(bookId) {
    router.push(`/books/${bookId}/edit`)
}

onMounted( async ()=>{
    await fetchBooksAndPush()
}
)

</script>

<template>
    <input type="file" id="file-input" accept=".txt" @change="handleFileChange"/>
    <main>
        <label for="file-input" class="document-container add-document">
        <form method="post" id="file-form" action enctype="multipart/form-data" @submit.prevent="handleSubmit">
            <div v-show="files === null">+</div>
            <!-- todo 加上颜色前后变换 -->
            <div>{{newTitle}}</div>
            <button class="material-icons" v-if="files != null">upload_file</button>
        </form>
        </label>
        <article class="document-container" v-for="document in books" @click.self="viewBook(document.id)" @mouseenter="document.isHover=1" @mouseleave="document.isHover=0">
            <div class="document-title">{{document.title}}</div>
            <div class="button-group">
                <button class="material-icons" @click="deleteBook(document.id)">delete</button>
                <button class="material-icons" @click="editBook(document.id)">edit</button>
            </div>
        </article>
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
    font-size: 2rem;
    font-family: Alice;
    text-align: center;
}

input {
    opacity: 0;
}

.document-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 3px solid var(--border-color);
    border-radius: var(--border-radius);
    box-shadow: 4px 4px 0 0 var(--border-color);
    padding: 2rem;
    align-self: center;
    justify-self: center;
    width: 14vw;
    height: 40vh;
    transition: border-color 200ms ease-in-out;
}

.document-container:hover {
    border-color: var(--book-color);
}

.add-document {
    background-color: transparent;
    font-size: 2rem;
    border: 2px dashed hsl(92, 59%, 66%);
    color: var(--component);
    box-shadow: none;
    cursor: pointer;
}

.button-group {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    width: 100%;
    opacity: 0;
    transition: opacity 200ms ease-in-out;
}

button {
    margin-top: 2rem;
    padding: 1rem;
    font-size: 2rem;
}

.button-group:hover {
    opacity: 1;
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