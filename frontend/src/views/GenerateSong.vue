<template>
  <div class="container">
    <div class="header">
      <back-button class="back-arrow"/>
      <h2 class="title">Generate Song</h2>
    </div>
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
      <textarea v-model="prompt" placeholder="Lyrics" 
               class="lyrics" rows="6"></textarea>
      </div>

      <div class="checkbox">
        <label class="checkbox">
          <input type="checkbox" v-model="customMode" /> Custom Mode
        </label>
        <label>
          <input type="checkbox" v-model="instrumental" /> Instrumental
        </label>
      </div>

      <div class="dropdown">
        <label for="model">Select Model:</label>
        <select id="model" v-model="selectedModel">
          <option value="V3_5" selected>V3_5</option>
          <option value="V4">V4</option>
          <option value="V4_5">V4_5</option>
        </select>
      </div>
      

      <button class="">
        Generate
      </button>
    </form>
      
    <div v-if="songs.length">
      <SongCard v-for="song in songs" :key="song.id" :song="song" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import BackButton from "@/components/BackButton.vue";
import SongCard from '@/components/SongCard.vue'

const prompt = ref('')
const style = ref('')
const title = ref('')
const customMode = ref(false)
const instrumental = ref(false)
const result = ref('')
const selectedModel = ref('V3_5')
const songs = ref([])

// Optional: clear style/title when customMode off
watch(customMode, (newVal) => {
  if (!newVal) {
    style.value = ''
    title.value = ''
  }
})

const submit = async () => {
  try {
    console.log("in submit")
    let url = 'http://localhost:8000/generate-song'
    const payload = {
      prompt: prompt.value,
      customMode: customMode.value,
      instrumental: instrumental.value,
      model: selectedModel.value
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
    console.log("Sending results")
    const res = await axios.post(url, payload)
    const sunoData = res.data?.data?.response?.sunoData || []
    songs.value = sunoData
    console.log("Back with results")
    const taskId = res.data?.data?.taskId

    // Sla alle titels op met dezelfde taskId
    if (taskId) {
      sunoData.forEach(song => {
        if (song.title) {
          localStorage.setItem(song.title, taskId)
        }
      })
    }

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
