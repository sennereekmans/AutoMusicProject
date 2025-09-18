<template>
  <div class="container">
    <h1 class="title">🎵 AutoMusicProject 🎵</h1>
    <h2>Select a feature:</h2>
    <div class="links">
      <router-link to="/lyrics" class="link-button">Generate Lyrics</router-link>
      <router-link to="/generate-song" class="link-button">Generate Song</router-link>
      <router-link to="/generate-video" class="link-button">Generate Videoclip</router-link>
      <router-link to="/credits" class="link-button">View Credits</router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style>
.container {
  max-width: 600px;
  margin: 60px auto;
  padding: 30px;
  background-color: #1e1e1e;
  border-radius: 12px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container form{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.container form input{
    margin-bottom: 10px;
    padding: 5px; 
    border-radius: 10px; 
    width: 300px;
}

.container form input[type="checkbox"] {
  width: auto;
}


.container form label{
    display: flex;
    flex-direction: row;
    margin-bottom: 10px;
}

.container form label input{
    margin-right: 5px;
}

.title {
  color: #ffffff;
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.links {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.link-button {
  display: block;
  padding: 12px 20px;
  background-color: #0077cc;
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background-color 0.2s;
  margin: auto;
}

.link-button:hover {
  background-color: #005fa3;
}
</style>
