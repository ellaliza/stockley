<script setup lang="ts">
import { Icon } from '@iconify/vue';
import logo from '../assets/stockley_logo_only-removebg-preview.png';
import logo_text from '../assets/stockley_text_dark-removebg-preview.png';
</script>

<template>
    <aside>
        <div class="brand">
            <div class="logo" :style="{ backgroundImage: `url(${logo})` }"></div>
            <div class="brand-text" :style="{ backgroundImage: `url(${logo_text})` }"></div>
        </div>
        <nav>
            <RouterLink to="/">
                <div class="active">
                    <Icon icon="mingcute:grid-2-line" width="22" height="22" />
                    <p class="nav-link">Dashboard</p>
                </div>
            </RouterLink>
            <RouterLink to="/products"><div>
                <Icon icon="solar:box-linear" width="22" height="22" />
                <p class="nav-link">Products</p>
            </div></RouterLink>
            <RouterLink to="/inventory"><div>
                <Icon icon="streamline-ultimate:warehouse-storage-2" width="22" height="22" />
                <p class="nav-link">Inventory</p>
            </div></RouterLink>
        </nav>
    </aside>
</template>

<style scoped>

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
.brand{
    display: flex;
    align-items: center;
}
.nav-link{
    color: whitesmoke
}
aside{
    background-color: var(--sidebar);
    color: var(--light);
    position: sticky;
    top: 0rem;
    align-self: flex-start;
    min-width: 13rem;
    height: 100svh; /* 5rem is approximate header height */
    overflow-y: auto;
    color: var(--deep-blue-60);
    padding: 1rem;
    font-size: small;
}
nav div{
    padding: 0.5rem;
    display: grid;
    grid-template-columns: 1fr 4fr;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
nav div:hover{
    background-color: var(--deep-blue-10);
    color: var(--teal-80)
}
@media (max-width: 768px){
    aside{
        display: none;
    }
}
.active{
    background-color: var(--sidebar-primary);
}
</style>