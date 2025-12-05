<script setup lang="ts">
import { Icon } from '@iconify/vue';

</script>

<template>
    <aside>
        <nav>
            <RouterLink to="/"><div>
                <Icon icon="mingcute:grid-2-line" width="22" height="22" />
                <p>Dashboard</p>
            </div></RouterLink>
            <RouterLink to="/products"><div>
                <Icon icon="solar:box-outline" width="22" height="22" />
                <p>Products</p>
            </div></RouterLink>
            <RouterLink to="/inventory"><div>
                <Icon icon="streamline-ultimate:warehouse-storage-2" width="22" height="22" />
                <p>Inventory</p>
            </div></RouterLink>
        </nav>
    </aside>
</template>

<style scoped>

aside{
    background-color: var(--stockley-deep-blue);
    color: var(--light);
    position: sticky;
    top: 5rem;
    align-self: flex-start;
    min-width: 13rem;
    height: calc(100vh - 5rem); /* 5rem is approximate header height */
    overflow-y: auto;
    color: var(--deep-blue-60);
    padding: 1rem;
}
nav div{
    padding: 0.8rem;
    display: grid;
    grid-template-columns: 1fr 4fr;
    align-items: center;
    justify-content: center;
    border-radius: 1rem;
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
</style>