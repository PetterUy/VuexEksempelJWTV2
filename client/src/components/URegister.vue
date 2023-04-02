<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="register">
        <label for="email">
          <input
            type="email"
            id="email"
            v-model="credentials.email"
            placeholder="email"
            required
          />
        </label>
        <label for="username">
          <input
            type="text"
            id="username"
            v-model="credentials.username"
            placeholder="username"
            required
          />
        </label>
        <label for="password">
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            placeholder="password"
            required
          />
        </label>
        <button type="submit">Register</button>
      </form>
    </div>
  </template>

<script>
import axios from 'axios';

export default {
  setup() {
    const credentials = {
      email: '',
      username: '',
      password: '',
    };

    async function register() {
      try {
        const response = await axios.post('http://localhost:5000/api/register', credentials);
        if (response.data.status === 'success') {
          alert('Registration successful');
          // Redirect to login or another desired page after successful registration
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        alert('Registration failed');
      }
      credentials.email = '';
      credentials.username = '';
      credentials.password = '';
    }

    return {
      credentials,
      register,
    };
  },
};
</script>
