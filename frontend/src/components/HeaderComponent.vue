<script setup lang="ts">
import { ref } from 'vue'
import logo from '../assets/stockley_logo_only.png'
import logo_text from '../assets/stockley_text.png'
import { Icon } from '@iconify/vue'

interface HeaderProps {
  pageTitle?: string
}

defineProps<HeaderProps>()
</script>


<template>
    <header>
        <div class="page" >{{ pageTitle ? pageTitle : "Dashboard"}}</div>

        <div class="search">

        </div>
        <div class="options">
            <Icon icon="mingcute:notification-line" />
            <!-- <Icon icon="ic:twotone-mode-night" width="18" height="18" /> -->
            <div class="user-initial">G</div>
        </div>
        <div class="user">
            <div class="user-initial">
                G
            </div>
            <div class="user-name">
                Guest
            </div>
        </div>
        <div class="menu">
            <Icon icon="ion:menu" width="20" height="20"  style="color: var(--grey-shade-80);" />
        </div>
        
    </header>
</template>

<style scoped>
header {
    padding: 0.5rem 1rem;
    background-color: var(--pure-white );
    display: grid;
    grid-template-columns: repeat(24, 1fr);
    align-items: center;
    position: sticky;
    top: 0%;
    left: 0%;
}
.page{
    padding-left: 2rem;
    font-size: medium;
    font-weight: 400;
}
.options{
    grid-column: 23/span 3;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    gap: 0.6rem;
}
.logo {
    height: 3rem;
    aspect-ratio: 1 / 1;
    background-size: cover;
    background-position: center;
    display: inline-block;
    grid-column: 1/span 1;

}
.brand-text{
    height: 3rem;
    aspect-ratio: 3/1;
    background-size: cover;
    display: inline-block;
    grid-column: 2/span 3;
}


.user {
    grid-column: 21/span 3;
    display: none;
    grid-template-columns: repeat(5, 1fr);
    color: white;
    background-image: linear-gradient(135deg, lightblue, #3d99a9, var(--stockley-deep-blue));
    padding: 0.2rem 0.7rem;
    border-radius: 0.7rem;
    align-items: center;
    min-width: 7rem;
}
.user-initial{
    
    padding: 0.2rem;
    text-align: center;
    background-color: var(--stockley-teal);
    border-radius: 50%;
    aspect-ratio: 1/1;
    vertical-align: middle;
    width: 2rem;
    scale: 0.7;
    color: var(--teal-80);
    
}
.user-name{
    grid-column: 3/span 2;
    padding: 0.2rem;
    text-align: center;
}
.menu{
    grid-column: 23/span 1;
    display: none;
}
@media (max-width: 768px){
    .brand-text, .user{
        display: none;
    }
    .menu{
        display: block;
    }
    
}
</style>
