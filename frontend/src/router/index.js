import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import GenerateSong from '../views/GenerateSong.vue'
import LyricsGenerator from '../views/LyricsGenerator.vue'
import Credits from '../views/Credits.vue'
import VideoGenerator from '../views/VideoGenerator.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/generate-song', name: 'GenerateSong', component: GenerateSong },
  { path: '/lyrics', name: 'LyricsGenerator', component: LyricsGenerator },
  { path: '/credits', name: 'Credits', component: Credits },
  { path: '/generate-video', name: 'GenerateVideo', component: VideoGenerator },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router

