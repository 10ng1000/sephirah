<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { toast} from 'vue-sonner';
import axios from 'axios'
import {useFloating, offset} from '@floating-ui/vue';

const props = defineProps({
    id: String,
    title: String,
    linkedChatSessions: Array
})

const router = useRouter()
const Files = ref(null)
const isHover = ref(false)
const isLink = ref(false)

const showTooltip = ref(false)
const toggle = ref(null)
const tooltip = ref(null)
const { floatingStyles } = useFloating(toggle, tooltip, {
  placement: 'top',
  middleware: [offset(40)]
})

function handleFileChange() {
    const input = document.getElementById('edit-book')
    Files.value = input.files
}

async function editBook(){
    const formData = new FormData()
    formData.append("file", Files.value[0])
    //发送表单信息
    axios.post(`api/books/${props.id}`,formData).then(
        () => {
            Files.value = null
            router.go(0)
        }
    )
}

function deleteBook() {
    toast.error('确定删除该文档吗？', {
        action: {
            label: '确定',
            onClick: async () => {
                axios.delete(`api/books/${String(props.id)}`).then(
                    response => {
                        if (response.status != 204) {
                            toast.success("删除成功")
                            router.go(0)
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

function viewBook() {
    //跳转路由
    router.push(`/books/${props.id}`)
}

</script>

<template>
    <article @click.self="viewBook()" @mouseenter="isHover = true" @mouseleave="isHover = false">
        <input type="file" id="edit-book" accept=".txt" @change="handleFileChange" />
        <input type="checkbox" id="check" v-model="isLink"/>
        <label class="toggle-button" for="check" ref="toggle" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false"></label>
        <div class="tooltip" ref="tooltip" :style="floatingStyles" v-if="showTooltip">链接到当前对话</div>
        <div class="document-title">{{ props.title }}</div>
        <div class="button-group">
            <label class="book-button material-icons" for="edit-book">edit</label>
            <form method="post" action enctype="multipart/form-data" @submit.prevent="editBook()"
                v-if="Files != null">
                <button class="book-button material-icons">upload_file</button>
            </form>
            <button class="book-button material-icons" @click="deleteBook()">delete</button>
        </div>
    </article>
</template>

<style scoped>
article {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  border: 3px solid var(--border-color);
  border-radius: var(--border-radius);
  box-shadow: 4px 4px 0 0 var(--border-color);
  padding: 2rem;
  align-self: center;
  justify-self: center;
  cursor: pointer;
  transition: border-color 200ms ease-in-out;
}
.toggle-button {
    margin-left: 75%;
    position: relative;
    width: 3rem;
    height: 1.5rem;
    border-radius: 3rem;
    background-color: var(--border-color);
    cursor: pointer;
    transition: background-color 200ms ease-in-out;
}

.toggle-button::before {
    content: '';
    position: absolute;
    left: 0;
    margin: 0.1rem;
    width: 1.3rem;
    height: 1.3rem;
    border-radius: 3rem;
    background-color: var(--hover-color);
    transition: transform 200ms ease-in-out;
}

input[type="checkbox"]:checked + .toggle-button {
    background-color: var(--text-jump-color);
}

input[type="checkbox"]:checked + .toggle-button::before {
    transform: translateX(1.5rem);
}

.document-title {
    font-size: 2rem;
    font-family: Alice;
    text-align: center;
    margin-top: 3rem;
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
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
.button-group:hover {
    opacity: 1;
}

</style>