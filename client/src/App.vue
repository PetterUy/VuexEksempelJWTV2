<template>
  <nav class="navbar navbar-expand-lg navbar-grey bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">The Robot Game</router-link>
      <button class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item" v-if="!loggedin">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item" v-if="!loggedin">
            <router-link to="/register" class="nav-link">Register</router-link>
          </li>
          <li class="nav-item" v-if="loggedin">
            <router-link to="/profile" class="nav-link">Profile</router-link>
          </li>
          <li class="nav-item" v-if="loggedin">
            <router-link to="/play" class="nav-link">Play</router-link>
          </li>
          <button v-if="loggedin" @click="logout">Log out</button>
        </ul>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

// Import the Bootstrap CSS file
import 'bootstrap/dist/css/bootstrap.css';

// Import the Bootstrap JS file
import 'bootstrap/dist/js/bootstrap.bundle';

export default {
  setup() {
    const store = useStore();
    const loggedin = computed(() => store.state.loggedin);
    const router = useRouter();

    function logout() {
      localStorage.removeItem('AToken');
      localStorage.removeItem('RToken');
      store.commit('logout');
      router.push('/');
    }

    return {
      loggedin,
      logout,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
  background-color: #252323;
  color: #fff;
}
</style>
