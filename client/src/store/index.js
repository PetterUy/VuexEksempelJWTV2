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
    },
    logout(state) {
      state.loggedin = false;
      state.username = '';
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
    logout({ commit }) {
      commit('logout');
    },
  },
});
