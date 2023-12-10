import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Users from '../views/Users.vue';
import Logout from '../views/Logout.vue';

const routes = [
  { path: '/login', component: Login },
  { path: '/users', component: Users },
  { path: '/logout', component: Logout },
  // ... otras rutas
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
