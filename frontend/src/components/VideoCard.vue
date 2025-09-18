<template>
  <div class="video-card">
    <h3>{{ video.title || "Music Video" }}</h3>
    <video :src="video.url" controls class="video-player"></video>
  </div>
</template>

<script setup>
const props = defineProps({
  video: {
    type: Object,
    required: true
  }
})
</script>

<style>
.video-card {
  border: 1px solid #444;
  background-color: #111;
  color: #eee;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
}

.video-player {
  width: 100%;
  max-height: 400px;
  margin-top: 0.5rem;
  border-radius: 8px;
  background: black;
}
</style>
