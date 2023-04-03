<template>
    <div>
        <p v-if="username">
            Welcome {{ username }} this is the ultimate awesome game that you wanna play!
        </p>
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
