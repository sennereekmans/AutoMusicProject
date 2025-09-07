<template>
  <div class="container">
        <div class="header">
      <back-button class="back-arrow"/>
      <h2 class="title">Credits</h2>
    </div>
    <button @click="getCredits" class="bg-green-500 text-white px-2 py-1 mb-2">Check Credits</button>
    <pre>{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import BackButton from "@/components/BackButton.vue";

const result = ref('')

const getCredits = async () => {
  try {
    const res = await axios.get('http://localhost:8000/credits')
    result.value = JSON.stringify(res.data, null, 2)
  } catch (e) {
    result.value = e.response?.data || e.message
  }
}
</script>
