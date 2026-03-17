<template>

<div>
    <h2>API</h2>
    <p>{{error}}</p>
    <div class="">
        <ul>
            <li v-for="book in books" :key="book.external_id">
                <h3>{{book.title}} - {{book.author}}</h3>
                <li v-for="review in book.reviews" class="review">
                    <p>{{review.rating}}</p>
                    <p>{{review.text}}</p>
                </li>
            </li>
        </ul>
    </div>
</div>

</template>



<script setup>

import axios from 'axios';
import { ref, onMounted } from 'vue';

const API = 'http://localhost:8000/books'
const books = ref(null)
const error = ref(null)

async function getBooks() {
  try {
    const res = await axios.get(API)
    books.value = res.data
  } catch (e) {
    error.value = e.message
  }
}

onMounted(() => {
  getBooks()
})

</script>


<style>
.review {
    padding-left: 25px;
    list-style: none
}
</style>
