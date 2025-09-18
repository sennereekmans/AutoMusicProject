# AutoMusicProject 🎵🤖

AutoMusicProject is a modern web application that allows users to generate complete music productions, from **lyrics to music video**, fully automated using AI models from [Suno API](https://sunoapi.org/). The project combines state-of-the-art web development with powerful AI integrations and is designed to provide a smooth, interactive experience.

---


## Demo
### Demo-video
[![Bekijk de demo](https://img.youtube.com/vi/fnBoELN9WsA/hqdefault.jpg)](https://www.youtube.com/watch?v=fnBoELN9WsA)

### Music-example
[![Listen to the example](https://img.youtube.com/vi/YHf7ELcRE3g/hqdefault.jpg)](https://www.youtube.com/watch?v=YHf7ELcRE3g)


 ---


## Features

- **Lyrics Generation:** Create unique song lyrics based on a topic of your choice.
- **Song Creation:** Generate a complete song using the generated lyrics and select your preferred music genre.
- **Music Video Generation:** Automatically create a matching music video for your song.
- **Credit Management:** Check your remaining Suno account credits to manage usage.

---

## Technologies

AutoMusicProject is built with a modern and scalable tech stack:

- **Backend:** Python with FastAPI for a fast and reliable API.
- **Frontend:** Vue.js for an interactive and dynamic user experience.
- **HTTP Requests:** Axios for communication between frontend and backend.
- **Containerization:** Docker for easy deployment and consistent development environment.
- **AI Integration:** Suno API for leveraging powerful music and video models.

---

## How the Application Works (Normal Flow)

1. **Lyrics Generation**  
   - The user inputs a topic for the song.  
    The backend sends the prompt to the Suno API and receives the generated lyrics.
    ![generate lyrics](readme-media/lyrics.png)
2. **Song Creation**  
   - Based on the lyrics, the user selects a music genre.  
   - The backend generates the song using the selected genre and lyrics.
    ![generate lyrics](readme-media/song1.png)
    ![generate lyrics](readme-media/song2.png)
    ![generate lyrics](readme-media/song3.png)

3. **Music Video Generation**  
   - With the generated song, the user can create a music video.  
   - The video is generated via the Suno API and can be viewed immediately.
    ![generate lyrics](readme-media/musicvideo.png)

4. **Credit Management**  
   - The user can check remaining Suno API credits to keep track of usage.
    ![generate lyrics](readme-media/credits.png)

---

## Installation and Setup

```bash
git clone https://github.com/sennereekmans/AutoMusicProject.git
cd AutoMusicProject
docker-compose up --build
```
