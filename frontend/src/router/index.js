import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import GenerateSong from '../views/GenerateSong.vue'
import ExtendMusic from '../views/ExtendMusic.vue'
import UploadCover from '../views/UploadCover.vue'
import LyricsGenerator from '../views/LyricsGenerator.vue'
import Credits from '../views/Credits.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/generate-song', name: 'GenerateSong', component: GenerateSong },
  { path: '/extend-music', name: 'ExtendMusic', component: ExtendMusic },
  { path: '/upload-cover', name: 'UploadCover', component: UploadCover },
  { path: '/lyrics', name: 'LyricsGenerator', component: LyricsGenerator },
  { path: '/credits', name: 'Credits', component: Credits },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router

