<script lang="ts" setup>
    import { Icon } from '@iconify/vue';
    defineProps({
        label: String,
        value: String,
        stat: String,
        icon: String,
    })

</script>
<template>
    <div class="card">
        <p class="label">{{label}}</p>
        <p class="value">{{value}}</p>
        <div class="status">
            <Icon icon="iconamoon:trend-up-bold" width="16" height="16" />
            <span>{{stat}}</span>
        </div>
    </div>
</template>
<style scoped>
/* box-shadow: 0.05rem 0.05rem 0.4rem var(--grey-40); */

.label{
    color: var(--grey-shade-10);
    font-size: small;
}
.value{
    color: var(--grey-shade-60);
    font-size: 20px;
}
.status{
    background-color: var(--stockley-teal);
    color: var(--white-30);
    padding: 0 0.5rem 0 0.3rem;
    border-radius: 1rem;
    min-width: 4.5rem;
    align-items: center;
    display: inline-flex;
    gap: 0.55rem;
    font-size: 8px;
    
}
.card{
    padding: 1rem;
    box-shadow: 0.05rem 0.05rem 0.4rem var(--grey-60);
    border-radius: 0.5rem;
}
.card:hover{
    box-shadow: 0.05rem 0.05rem 0.4rem var(--grey-40);
}

</style>