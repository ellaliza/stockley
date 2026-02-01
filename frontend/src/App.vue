<script setup lang="ts">
import {ref} from 'vue';
const name = ref("Ella");
const emoji = ref("😃");
import HeaderComponent from '@/components/HeaderComponent.vue';

import { RouterView, useRoute, useRouter } from 'vue-router';
import Sidebar from './components/Sidebar.vue';
const pageTitle = ref("");
const setPageTitle = (val: string) => pageTitle.value = val;

const router = useRouter()
const route = useRoute()

</script>

<template>
  <div class="app-shell">
    <Sidebar />
  
    <div class="content">
      <HeaderComponent :pageTitle="pageTitle"/>
      <main>
        <RouterView @emitPageTitle="setPageTitle"/>
      </main>
    </div>
  </div>
</template>

<style scoped>
.content{
  display: grid;
  grid-template-rows: 3rem auto;
  
  
}
.app-shell{
  height: 100vh;
  display: flex;
  flex-direction: row;
}
main{
  flex: 1;
  flex-grow: 2;
  overflow-y: auto;
  padding: 0.2rem 1rem;
  background-color: var(--background);
}
</style>
