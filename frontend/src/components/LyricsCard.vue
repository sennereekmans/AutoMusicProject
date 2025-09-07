<template>
  <div class="song-card">
    <h3>{{ song.title }}</h3>
    <p><strong>Lyrics:</strong></p>
    <pre class="lyrics">{{ song.text }}</pre>
  </div>
</template>

<script setup>
const props = defineProps({
  song: {
    type: Object,
    required: true
  },
})
</script>

<style>
.song-card {
  border: 1px solid #444;
  background-color: #111;
  color: #eee;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
}

.cover {
  width: 200px;
  height: 200px;
  object-fit: cover;
  display: block;
  margin: 0.5rem auto;
}

.lyrics {
  white-space: pre-wrap;
  padding: 0.5rem;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

audio {
  width: 100%;
}

audio::-webkit-media-controls-panel {
  background-color: #3e3e3e;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #666;
}

::-webkit-scrollbar-track {
  background: #111;
}
</style>
