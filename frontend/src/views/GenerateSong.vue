<template>
  <div class="container">
    <h2 class="title">Generate Song</h2>
    <form @submit.prevent="submit">
      <div v-if="!customMode" class="">
        <input v-model="prompt" placeholder="Prompt" 
              class="" />
      </div>


      <div v-if="customMode" class="">
        <input v-model="title" placeholder="Title" 
               class="" />
        <input v-model="style" placeholder="Style" 
               class="" />
        <input v-model="prompt" placeholder="Lyrics" 
              class="lyrics" />
      </div>

      <div class="checkbox">
        <label class="checkbox">
          <input type="checkbox" v-model="customMode" /> Custom Mode
        </label>
        <label>
          <input type="checkbox" v-model="instrumental" /> Instrumental
        </label>
      </div>

      

      <button class="">
        Generate
      </button>
    </form>

    <pre class="">{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const prompt = ref('')
const style = ref('')
const title = ref('')
const customMode = ref(false)
const instrumental = ref(false)
const result = ref('')

// Optional: clear style/title when customMode off
watch(customMode, (newVal) => {
  if (!newVal) {
    style.value = ''
    title.value = ''
  }
})

const submit = async () => {
  try {
    let url = 'http://localhost:8000/generate-song'
    const payload = {
      prompt: prompt.value,
      customMode: customMode.value,
      instrumental: instrumental.value
    }

    if (customMode.value) {
      url = 'http://localhost:8000/generate-customsong'
      payload.style = style.value
      payload.title = title.value
      if (!instrumental.value) {
        payload.prompt = prompt.value
      } else {
        delete payload.prompt
      }
    }

    const res = await axios.post(url, payload)
    result.value = JSON.stringify(res.data, null, 2)
  } catch (e) {
    result.value = e.response?.data || e.message
  }
}
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
input {
  display: block;
}


</style>
