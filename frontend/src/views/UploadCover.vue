<template>
  <div class="container">
        <div class="header">
      <back-button class="back-arrow"/>
      <h2 class="title">Upload & Cover</h2>
    </div>
    <form @submit.prevent="submit">
      <input v-model="uploadUrl" placeholder="Upload URL" class="border p-1 mb-2 w-full"/>
      <input v-model="prompt" placeholder="Prompt" class="border p-1 mb-2 w-full"/>
      <input v-model="style" placeholder="Style" class="border p-1 mb-2 w-full"/>
      <input v-model="title" placeholder="Title" class="border p-1 mb-2 w-full"/>
      <label>
        <input type="checkbox" v-model="customMode"/> Custom Mode
      </label>
      <label>
        <input type="checkbox" v-model="instrumental"/> Instrumental
      </label>
      <button class="bg-blue-500 text-white px-2 py-1 mt-2">Upload & Cover</button>
    </form>
    <pre>{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import BackButton from "@/components/BackButton.vue";

const uploadUrl = ref('')
const prompt = ref('')
const style = ref('')
const title = ref('')
const customMode = ref(false)
const instrumental = ref(false)
const result = ref('')

const submit = async () => {
  try {
    const res = await axios.post('http://localhost:8000/upload-cover', {
      uploadUrl: uploadUrl.value,
      prompt: prompt.value,
      style: style.value,
      title: title.value,
      customMode: customMode.value,
      instrumental: instrumental.value
    })

    const taskId = res.data?.data?.taskId
    if (taskId) {
      localStorage.setItem(title, taskId)
    }
    
    result.value = JSON.stringify(res.data, null, 2)
  } catch (e) {
    result.value = e.response?.data || e.message
  }
}
</script>
