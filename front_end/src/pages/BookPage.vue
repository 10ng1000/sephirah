<script setup>
import {ref, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import { Marked } from "marked";
import { markedHighlight } from "marked-highlight";
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import 'github-markdown-css/github-markdown.css';
import axios from 'axios'
import autosize from 'autosize';

const marked = new Marked(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang, info) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext';
      return hljs.highlight(code, { language }).value;
    }
  })
);

const route = useRoute()
const router = useRouter()
const bookId = ref(route.params.book_id)
const book = ref({
    title: '',
    text: ''
})
const edit = ref(route.path.endsWith('edit'))

function getBookText(bookId) {
    axios.get(`api/books/${String(bookId)}`).then(
        response => {
            console.log(response.data.text)
            book.value = response.data
        }
    )
}

onMounted(()=>{
    getBookText(bookId.value)
    autosize(document.querySelectorAll('textarea'));
})

</script>

<template>
    <main>
        <article>
            <button class="back-button material-icons" @click="router.back()">arrow_back</button>
            <h1>{{ book.title }}</h1>
            <div v-if="!edit" class="markdown-body" v-html="marked.parse(book.text)"></div>
        </article>
    </main>
</template>

<style scoped>
main {
    width: 100%;
    height: 100%;
}
article {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    border: var(--border);
    border-radius: var(--border-radius);
    margin: 3rem;
    min-height: 80%;
}

.back-button {
    align-self: flex-start;
    padding: 0.5rem;
    margin-top : 1rem;
    margin-left: 1rem;
}

div {
    padding-inline: 10%;
}
</style>