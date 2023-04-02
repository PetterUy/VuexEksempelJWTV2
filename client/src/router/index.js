import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ULogin from '../components/ULogin.vue';
import URegister from '../components/URegister.vue';
import UProfile from '../components/UProfile.vue';
import UPlay from '../components/UPlay.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'ULogin',
    component: ULogin,
  },
  {
    path: '/profile',
    name: 'UProfile',
    component: UProfile,
  },
  {
    path: '/play',
    name: 'UPlay',
    component: UPlay,
  },
  {
    path: '/register',
    name: 'URegister',
    component: URegister,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
