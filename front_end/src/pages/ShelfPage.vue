<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';

const url = ref(import.meta.env.VITE_BACKEND_URL + '/api/books/')
const files = ref(null)

const newTitle = computed(() => {
    if (!files.value) {
        return '上传知识'
    }
    return files.value[0].name
})

const hasFile = computed(() => {
    return files.value !== null
})

const books = ref([
    {title: 'Divina Commedia'},
    {title: '거울'},
    {title: '红楼梦'},
    {title: 'Moby Dick'},
    {title: '地獄変'},
    {title: 'Преступление и наказание'},
    {title: '从letme到严君泽'},
])

function addDocument() {
    books.value.push({title: 'Document ' + (books.value.length + 1)})
}

function handleFileChange() {
    const input = document.getElementById('file-input')
    files.value = input.files
}

async function handleSubmit(e){
    e.preventDefault()
    const formData = new FormData()
    formData.append("file", files.value[0])
    //发送表单信息
    const response = await fetch(url.value, {
        method: 'post',
        body: formData
        }
    )
    window.location.reload()
}

async function fetchBooksAndPush() {
    fetch(url.value).then(response => response.json()).then(
        data => {
            for (const book of data) {
                books.value.unshift(book)
            }
        }
    )
}

onMounted( async ()=>{
    fetchBooksAndPush()
}
)
</script>

<template>
    <input type="file" id="file-input" accept=".txt" @change="handleFileChange"/>
    <main>
        <label for="file-input" class="document-container add-document">
        <form method="post" id="file-form" enctype="multipart/form-data" :action="url" @submit="handleSubmit" target="_self">
            <div v-if="files === null">+</div>
            <!-- todo 加上颜色前后变换 -->
            <div>{{newTitle}}</div>
            <button class="material-icons" v-if="files != null">upload_file</button>
        </form>
        </label>
        <article class="document-container" v-for="document in books">
            <div class="document-title">{{document.title}}</div>
            <div></div>
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
    padding-top: 4rem;
    width: 80%;
    height: 100%;
    font-size: 2rem;
    font-family: Alice;
    text-align: center;
}

.document-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: var(--border);
    border-radius: var(--border-radius);
    padding: 2rem;
    align-self: center;
    justify-self: center;
    width: 14vw;
    height: 40vh;
}

input {
    opacity: 0;
    width: 0;
    height: 0;
}

.add-document {
    background-color: transparent;
    font-size: 2rem;
    border: 2px dashed #58cc02;
    color: var(--component);
    cursor: pointer;
}


button {
    margin-top: 2rem;
    padding: 1rem;
    font-size: 2rem;
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