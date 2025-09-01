<template>
  <div class="container">
    <h2 class="title">Generate Lyrics</h2>
    <form @submit.prevent="submit">
      <input v-model="prompt" placeholder="Prompt" class="border p-1 mb-2 w-full"/>
      <input v-model="callBackUrl" placeholder="Callback URL" class="border p-1 mb-2 w-full"/>
      <button class="bg-blue-500 text-white px-2 py-1 mt-2">Generate</button>
    </form>
    <pre>{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const prompt = ref('')
const callBackUrl = ref('')
const result = ref('')

const submit = async () => {
  try {
    const res = await axios.post('http://localhost:8000/lyrics', {
      prompt: prompt.value,
      callBackUrl: callBackUrl.value
    })
    result.value = JSON.stringify(res.data, null, 2)
  } catch (e) {
    result.value = e.response?.data || e.message
  }
}
</script>
