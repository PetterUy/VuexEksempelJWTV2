import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    loggedin: false,
    username: '',
  },
  mutations: {
    login(state, username) {
      state.loggedin = true;
      state.username = username;
      localStorage.setItem('username', username);
      localStorage.setItem('loggedin', true);
    },
    logout(state) {
      state.loggedin = false;
      state.username = '';
      localStorage.removeItem('username');
      localStorage.removeItem('loggedin');
    },
  },
  actions: {
    async login({ commit }, credentials) {
      const response = await axios.post('http://localhost:5000/api/login', credentials);
      if (response.data.status === 'success') {
        commit('login', credentials.username);
      } else {
        alert(response.data.message);
      }
    },
    loadStateFromLocalStorage({ commit }) {
      const username = localStorage.getItem('username');
      const loggedin = localStorage.getItem('loggedin');
      if (username && loggedin) {
        commit('login', username);
      } else {
        commit('logout');
      }
    },
    logout({ commit }) {
      commit('logout');
    },
  },
});
