<script setup lang="ts">
import {ref} from 'vue';
const name = ref("Ella");
const emoji = ref("😃");
import HeaderComponent from '@/components/HeaderComponent.vue';
import Home from '@/components/Home.vue';
import Products from '@/components/Products.vue';
import Inventory from './components/Inventory.vue';

import { RouterView } from 'vue-router';
import Sidebar from './components/Sidebar.vue';

</script>

<template>
  <div class="app-shell">
    <HeaderComponent />

    <div class="content">
      <Sidebar />
      <main>
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.content{
  display: flex;
  flex-grow: 1;
}
.app-shell{
  height: 100vh;
  display: flex;
  flex-direction: column;
}
main{
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: var(--grey-80);
}
</style>
