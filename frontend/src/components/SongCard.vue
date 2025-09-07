<template>
  <div class="song-card">
    <h3>{{ song.title }}</h3>
    <p><strong>Tags:</strong> {{ song.tags }}</p>
    <p><strong>Lyrics:</strong></p>
    <pre class="lyrics">{{ song.prompt }}</pre>
    <p><strong>Duration:</strong> {{ formatDuration(song.duration) }}</p>
    <img :src="song.imageUrl" alt="Cover" class="cover" />

    <audio :src="song.audioUrl" controls class="dark-audio"></audio>
  </div>
</template>

<script setup>
import AudioPlayer from 'vue3-audio-player'
import 'vue3-audio-player/dist/style.css'  // Import default styles

const props = defineProps({
  song: {
    type: Object,
    required: true
  }
})

const formatDuration = (seconds) => {
  const min = Math.floor(seconds / 60)
  const sec = Math.floor(seconds % 60)
  return `${min}:${sec < 10 ? '0' : ''}${sec}`
}
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
  margin: 0.5rem auto; /* center image */
}

.lyrics {
  white-space: pre-wrap; /* preserve \n newlines */

  padding: 0.5rem;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

audio {
  width: 100%;
}

audio::-webkit-media-controls-panel {
  background-color: #3e3e3e; /* Dark control bar */
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-thumb {
  background: #444; /* Dark gray */
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #666; /* Slightly lighter on hover */
}

::-webkit-scrollbar-track {
  background: #111; /* Dark background for track */
}
</style>
