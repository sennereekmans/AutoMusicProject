<template>
  <div class="back-button" @click="goHome">
    <img src="../assets/arrow.png" alt="Back" class="arrow-icon" />
  </div>
</template>

<script>
export default {
  name: "BackButton",
  methods: {
    goHome() {
      this.$router.push("/"); // Navigeer naar home route
    }
  }
};
</script>

<style scoped>
.back-button {
  display: inline;
  cursor: pointer;
  border-radius: 10px; 
}
.arrow-icon {
  width: 24px;
  height: 24px;
}
</style>
