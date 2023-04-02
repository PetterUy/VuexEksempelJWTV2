<template>
    <div>
      <h1 v-if="loggedin">Welcome, {{ username }}!</h1>
      <h1 v-if="!loggedin">Please log in to continue.</h1>
      <form v-if="!loggedin" @submit.prevent="login">
        <label for="username">
          <input type="text"
          placeholder = "email"
          id="username"
          v-model="credentials.username"
          required>
        </label>
        <label for="password">
          <input type="password"
          id="password"
          v-model="credentials.password"
          placeholder = "password"
          required>
        </label>
        <button type="submit">Log in</button>
      </form>
      <button v-if="loggedin" @click="logout">Log out</button>
    </div>
  </template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default {
  setup() {
    const store = useStore();

    const loggedin = computed(() => store.state.loggedin);
    const username = computed(() => store.state.username);

    const credentials = {
      username: '',
      password: '',
    };

    async function login() {
      const response = await axios.post('http://localhost:5000/api/login', credentials);
      if (response.data.status === 'success') {
        const { AToken, RToken } = response.data;
        localStorage.setItem('AToken', AToken);
        localStorage.setItem('RToken', RToken);
        store.commit('login', credentials.username);
      } else {
        alert(response.data.message);
      }
      credentials.username = '';
      credentials.password = '';
    }

    function logout() {
      localStorage.removeItem('AToken');
      localStorage.removeItem('RToken');
      store.commit('logout');
    }

    const axiosInstance = axios.create({
      baseURL: 'http://localhost:5000',
      timeout: 5000,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('AToken')}`,
        'Content-Type': 'application/json',
        accept: 'application/json',
      },
    });

    axiosInstance.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest.retry) {
          originalRequest.retry = true;
          const AToken = localStorage.getItem('AToken');
          const RToken = localStorage.getItem('RToken');
          console.log(AToken);

          const response = await axios.post('http://localhost:5000/api/RToken', { RToken });

          if (response.status === 200) {
            localStorage.setItem('AToken', response.data.AToken);
            axiosInstance.defaults.headers.common.Authorization = `Bearer ${response.data.AToken}`;
            return axiosInstance(originalRequest);
          }
        }
        return Promise.reject(error);
      },
    );

    setInterval(async () => {
      const RToken = localStorage.getItem('RToken');
      if (RToken) {
        const response = await axios.post('http://localhost:5000/api/RToken', { RToken });
        if (response.status === 200) {
          localStorage.setItem('AToken', response.data.AToken);
        }
      }
    }, 15 * 60 * 1000);

    return {
      loggedin,
      username,
      credentials,
      login,
      logout,
    };
  },
};
</script>
