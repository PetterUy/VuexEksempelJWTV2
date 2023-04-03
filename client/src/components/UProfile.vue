<template>
    <div>
      <h1>User Profile</h1>
      <p v-if="username">Logged in as: {{ username }}</p>
    </div>
  </template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    const username = computed(() => store.state.username);

    return {
      username,
    };
  },
};
</script>
