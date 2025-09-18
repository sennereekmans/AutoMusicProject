<template>
  <div class="container">
    <div class="header">
      <back-button class="back-arrow"/>
      <h2 class="title">Generate Lyrics</h2>
    </div>
    <form @submit.prevent="submit">
      <input v-model="prompt" placeholder="Prompt" class="border p-1 mb-2 w-full"/>
      <button class="bg-blue-500 text-white px-2 py-1 mt-2">Generate</button>
    </form>
    <div v-if="songs.length" class="mt-4">
      <LyricsCard
        v-for="(song, index) in songs"
        :key="index"
        :song="song"
      />
    </div>   
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import BackButton from "@/components/BackButton.vue";
import LyricsCard from "@/components/LyricsCard.vue";

const prompt = ref('')
const result = ref('')
const songs = ref([])

const submit = async () => {
  try {
    const res = await axios.post('http://localhost:8000/lyrics', {
      prompt: prompt.value,
    })
    
    const lyricsList = res.data?.data?.response?.data || []
    songs.value = lyricsList

    const taskId = res.data?.data?.taskId

    // Sla alle titels op met dezelfde taskId
    if (taskId) {
      lyricsList.forEach(song => {
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
