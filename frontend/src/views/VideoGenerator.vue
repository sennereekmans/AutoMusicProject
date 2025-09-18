<template>
  <div class="container">
    <div class="header">
      <back-button class="back-arrow"/>
      <h2 class="title">Generate Music Video</h2>
    </div>

    <form @submit.prevent="submit">
      <input v-model="taskId" placeholder="Task ID" />
      <input v-model="audioId" placeholder="Audio ID" />
      <input v-model="author" placeholder="Author (optional)" />
      <input v-model="domainName" placeholder="Domain Name (optional)" />

      <button>Generate Video</button>
    </form>

    <div v-if="videos.length">
      <VideoCard v-for="video in videos" :key="video.id" :video="video" />
    </div>
  </div>
</template>

<script setup>
    import { ref } from 'vue'
    import axios from 'axios'
    import BackButton from "@/components/BackButton.vue";
    import VideoCard from '@/components/VideoCard.vue'

    const taskId = ref('')
    const audioId = ref('')
    const author = ref('')
    const domainName = ref('')
    const result = ref('')
    const videos = ref([])

    const submit = async () => {
    try {
      const payload = {
        taskId: taskId.value,
        audioId: audioId.value,
      }
      if (author.value) payload.author = author.value
      if (domainName.value) payload.domainName = domainName.value

      const res = await axios.post("http://localhost:8000/generate-music-video", payload)

      const data = res.data?.data
      const url = data?.response?.videoUrl

      videos.value = url ? [{ id: data.taskId, url }] : []
      result.value = JSON.stringify(res.data, null, 2)
    } catch (e) {
      result.value = e.response?.data || e.message
    }
  }
</script>

<style>
input {
  display: block;
  margin: 0.5rem 0;
}
</style>
