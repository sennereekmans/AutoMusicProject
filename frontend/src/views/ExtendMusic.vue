<template>
  <div class="container">
    <h2 class="title">Extend Music</h2>
    <form @submit.prevent="submit">
      <input v-model="audioId" placeholder="Audio ID" class="border p-1 mb-2 w-full"/>
      <input v-model.number="continueAt" placeholder="Continue at (seconds)" type="number" class="border p-1 mb-2 w-full"/>
      <input v-model="prompt" placeholder="Prompt" class="border p-1 mb-2 w-full"/>
      <input v-model="style" placeholder="Style" class="border p-1 mb-2 w-full"/>
      <input v-model="title" placeholder="Title" class="border p-1 mb-2 w-full"/>
      <label>
        <input type="checkbox" v-model="defaultParamFlag"/> Custom Params
      </label>
      <button class="bg-blue-500 text-white px-2 py-1 mt-2">Extend</button>
    </form>
    <pre>{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const audioId = ref('')
const continueAt = ref(0)
const prompt = ref('')
const style = ref('')
const title = ref('')
const defaultParamFlag = ref(false)
const result = ref('')

const submit = async () => {
  try {
    const res = await axios.post('http://localhost:8000/extend-music', {
      audioId: audioId.value,
      continueAt: continueAt.value,
      prompt: prompt.value,
      style: style.value,
      title: title.value,
      defaultParamFlag: defaultParamFlag.value
    })
    result.value = JSON.stringify(res.data, null, 2)
  } catch (e) {
    result.value = e.response?.data || e.message
  }
}
</script>
