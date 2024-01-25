<script setup>
import { computed, onMounted, ref } from 'vue';
const sessions = ref([])

const groups = computed(() => {
    const g = {}
    sessions.value.forEach(session => {
        var date = new Date(session.start_time)
        // 转为东八区时间
        date.setHours(date.getHours() + 8)
        const key = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
        if (!g[key]) {
            g[key] = []
        }
        const formatter = new Intl.DateTimeFormat('zh-CN', {
            hour12: false,
            hour: 'numeric',
            minute: 'numeric'
        })
        const date_str = formatter.format(date)
        const new_session = {
            ...session,
            start_time: date_str
        }
        g[key].push(new_session)
    })
    return g
})

const fetchSessions = async () => {
    fetch(import.meta.env.VITE_BACKEND_URL + '/api/chat/sessions?isAllSessions=true')
        .then(response => response.json())
        .then(data => {
            sessions.value = data
        })
}
const deleteSessions = async () => {
    fetch(import.meta.env.VITE_BACKEND_URL + '/api/chat/sessions', {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            sessions.value = data
        })
}

onMounted(() => {
    fetchSessions()
})

</script>

<template>
    <q-page>
        <main>
        <section v-for="(group, key) in groups">
            <caption>{{ key }}</caption>
            <router-link v-for="session in group" :to="'/chat/'+session.session_id">
                <name>{{session.name}}</name>
                <date>{{session.start_time}}</date>
            </router-link>
        </section>
        </main>
    </q-page>
</template>

<style scoped lang="scss">
.q-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-center;
}

main {
    display: flex;
    flex-direction: column;
    align-items: sstretch;
    justify-content: flex-start;
    margin-inline: auto;
    width: 65%;
    height: 100%;
    overflow-y: scroll;
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
    width: 100%;
}

a {
    display: flex;
    flex-direction: row;
    margin-top: 1rem;
    border: $border;
    border-radius: $border-radius;
    padding: $border-padding;
    width: 100%;
    text-decoration: none;
    //不显示超链接的颜色
}

name {
    max-width: 80%;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;   
}

date {
    margin-left: auto;
}


</style>