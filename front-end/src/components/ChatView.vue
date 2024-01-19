<script setup>
import { ref, defineCustomElement} from 'vue';
import 'deep-chat';
import HtmlMessage from './HtmlMessage.ce.vue';
import { Toaster} from 'vue-sonner';
import { onMounted } from 'vue';
import { nextTick } from 'vue';

const chat = ref(null);
onMounted(() => {
  //注册自定义组件
  const HtmlMessageElement = defineCustomElement(HtmlMessage);
  customElements.define('html-message', HtmlMessageElement);
  nextTick(() => {
    chat.value.addEventListener('new-message', (e) => {
      console.log(e.detail);
      chat.value.scrollToBottom()
    });
  });

})

//欢迎信息
const messages = ref([
  { "role": "ai" , "html": '<html-message text="你好，我是sephirah，请问有什么我可以帮忙的吗？" end="true"></html-message>'}
])

//自定义的response拦截器，用于将后端返回的数据转换为deepchat需要的格式，往下的request拦截器同理
const now_message = ref('')
function responseInterceptor (response) {
    if (response.end != true) {
      now_message.value += response.message
      //chat.value.scrollToBottom()
      //等待0.01秒，让deepchat的scrollToBottom生效
      setTimeout(() => {
        chat.value.scrollToBottom()
      }, 1);
      return {html: `<html-message text='${now_message.value}' end='false'></html-message>`, overwrite: true}
      //return {text: `${response.message}`}
    }
    else {
      const ret = {html: `<html-message text='${now_message.value}' end='true'></html-message>`, overwrite: true}
      now_message.value = ''
      return ret
    }
  }
function requestInterceptor (request) {
    request.body = {message: request.body.messages[0].text}
    return request
  }
</script>


<template>
  <Toaster />
  <deep-chat
    ref="chat"
    :request='{
      "url": "http://localhost:8000/chat/sse_invoke",
      "method": "POST",
      "headers": { "Content-Type": "application/json" },
    }'
    :responseInterceptor='responseInterceptor'
    :requestInterceptor='requestInterceptor'
    stream= true
    style="
    width: 100%;
    border: 0px;
    height: 90vh;
    border-radius: 0.5rem;
    border-color: #e4e4e4;
    font-size: medium;
    margin-top: 5vh;" :textInput='{
      "styles": {
        "container": {
          "borderRadius": "0.7rem",
          "border": "unset",
          "width": "80%",
          "textAlign": "center",
          "boxShadow": "0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)",
        },
        "text": {
          "padding": "1rem",
          "fontSize": "1rem",
          "margin-left": "1rem",
          "margin-right": "2rem",
         }
      },
      "placeholder": { "text": "Ask me anything...", "style": { "color": "#606060" } }
    }'
  :messageStyles='{
  "default": {
    "loading": {
      "bubble": { "backgroundColor": "#3793ff", "fontSize": "20px", "color": "white" }
    },
    "shared": {
      "innerContainer": {"width": "auto"},
      "bubble": {
        "backgroundColor": "unset",
        "max-width": "70%",
        "boxShadow": "0px 0.3px 0.9px rgba(0, 0, 0, 0.12), 0px 1.6px 3.6px rgba(0, 0, 0, 0.16)",
        "color" : "#4b4b4b"
      }
    },
    "user": {
      "bubble": {
        "background": "#ffffff",
        "marginRight": "10%",
      }
    },
    "ai": { "bubble": { "background": "#ffffff", "marginLeft": "10%" } }
  }
}' :submitButtonStyles='{
  "position": "inside-right",
  "submit": {
    "container": {
      "default": { "margin": "0.6rem 0.6rem", "borderRadius": "1rem", "backgroundColor": "unset"},
      "hover": { "backgroundColor": "#b0deff4f" },
      "click": { "backgroundColor": "#b0deffb5" }
    },
    "svg": {
      "content": "<?xml version=\"1.0\" encoding=\"utf-8\"?> <svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"m21.426 11.095-17-8A.999.999 0 0 0 3.03 4.242L4.969 12 3.03 19.758a.998.998 0 0 0 1.396 1.147l17-8a1 1 0 0 0 0-1.81zM5.481 18.197l.839-3.357L12 12 6.32 9.16l-.839-3.357L18.651 12l-13.17 6.197z\"/></svg>",
      "styles": {
        "default": {
          "width": "1.5em",
          "filter":
            "brightness(0) saturate(100%) invert(10%) sepia(86%) saturate(6044%) hue-rotate(205deg) brightness(100%) contrast(100%)"
        }
      }
    }
  },
  "loading": {
    "svg": {
      "styles": {
        "default": {
          "filter":
            "brightness(0) saturate(100%) invert(72%) sepia(0%) saturate(3044%) hue-rotate(322deg) brightness(100%) contrast(96%)"
        }
      }
    }
  },
  "stop": {
    "container": { "hover": { "backgroundColor": "#ededed94" } },
    "svg": {
      "styles": {
        "default": {
          "filter": "brightness(0) saturate(100%) invert(72%) sepia(0%) saturate(3044%) hue-rotate(322deg) brightness(100%) contrast(96%)"
        }
      }
    }
  }
}' :initialMessages='messages' />
</template>

<style scoped lang="scss">
#messages {
  margin-top: "10%";
}
</style>

