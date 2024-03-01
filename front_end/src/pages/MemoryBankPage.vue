<script setup>
import { computed, onMounted, ref } from 'vue';
import {toast, Toaster} from 'vue-sonner';
import {useChatSessionStore} from '../store/chatSession';
import { storeToRefs } from 'pinia';

const groups = ref({})
const {chatSession} = storeToRefs(useChatSessionStore())

async function fetchSessions()  {
    let sessions = []
    await fetch(import.meta.env.VITE_BACKEND_URL + '/api/chat/sessions')
        .then(response => response.json())
        .then(data => {
            sessions = data
        })

    sessions.forEach(session => {
        var date = new Date(session.start_time)
        // 转为东八区时间
        const key = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
        if (!groups.value[key]) {
            groups.value[key] = []
        }
        const formatter = new Intl.DateTimeFormat('zh-CN', {
            hour12: false,
            hour: 'numeric',
            minute: 'numeric'
        })
        const dateStr = formatter.format(date)
        const newSession = {
            ...session,
            start_time: dateStr,
            showDelete: false
        }
        groups.value[key].push(newSession)
    })
}
async function deleteSession(e, session_id) {
    e.preventDefault()
    toast.error('确定删除该会话吗？', {
        action: {
            label: '确定',
            onClick: async () => {
                await fetch(import.meta.env.VITE_BACKEND_URL + `/api/chat/sessions/${session_id}`, {
                    method: 'DELETE'
                })
                groups.value = {}
                chatSession.value = null
                fetchSessions()
            }
        },
    })
    
}
function switchShowDelete(session) {
    session.showDelete = !session.showDelete
}

onMounted(() => {
    fetchSessions()
})

</script>

<template>
    <main>
        <section v-for="(group, key) in groups">
            <caption>{{ key }}</caption>
            <router-link v-for="session in group" :to="'/chat/'+session.session_id" @mouseenter="switchShowDelete(session)" @mouseleave="switchShowDelete(session)" @click="chatSession=session.session_id">
                <span class="session-name">{{session.name}}</span>
                <span class="session-date" v-if="!session.showDelete">{{session.start_time}}</span>
                <button class="material-icons" @click="deleteSession($event,session.session_id)" v-if="session.showDelete">delete</button>   
            </router-link>
        </section>
    </main>
</template>

<style scoped>
.q-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-center;
}

main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 3vh;
    width: var(--main-width);
    height: 100%;
}

caption {
    align-self: flex-start;
    font-family: Alice;
    font-size: 2rem;
    font-weight: bold;
    margin: 1rem auto 0 0;
}

section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 80%;
}

a {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 1rem;
  border: var(--border);
  border-radius: var(--border-radius);
  padding: var(--border-padding);
  width: 100%;
  height: calc(var(--border-padding) * 2);
  text-decoration: none;
}

.session-name {
    max-width: 80%;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;   
}

.session-date {
    margin-left: auto;
}


button {
    margin-left: auto;
    margin-right: 0.5rem;
    border: none;
    padding: 0;
    font-size: 1.5rem;
}

button:hover {
    color: var(--danger);
}


</style>