import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Home from '@/pages/Home.vue';
import Products from '@/pages/Products.vue';
import Inventory from './pages/Inventory.vue';
import RegisterPage from './pages/RegisterPage.vue';
import { createMemoryHistory, createRouter } from 'vue-router';
import type {route} from './types.js'

const routes: route[] = [
  {path: '/', component: Home},
  {path: '/register', component: RegisterPage},
  {path: '/products', component: Products},
  {path: '/inventory', component: Inventory},

  
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})
createApp(App).use(router).mount('#app')
