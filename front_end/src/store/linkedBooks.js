import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useLinkedBooksStore = defineStore("linkedBooks", () => {
  const linkedBooks = ref([]);

  //更新绑定的书籍
  function updateLinkedBooks(chatSession) {
    linkedBooks.value = [];
    axios.get(`api/chat/sessions/${chatSession}/books`).then((response) => {
      response.data.forEach((book) => {
        linkedBooks.value.push(book.id);
      });
    });
  }

  return { linkedBooks, updateLinkedBooks };
});
