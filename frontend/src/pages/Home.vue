<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { Icon } from '@iconify/vue';
import type { DashboardData } from '@/types';
import { axiosInstance } from '@/api';
import { computed, onMounted, reactive, ref } from 'vue';
import SummaryCard from '@/components/SummaryCard.vue';
import type SummaryCardVue from '@/components/SummaryCard.vue';
import RecentStockTable from '@/components/RecentStockTable.vue';
import LowStockProductsTable from '@/components/LowStockProductsTable.vue';
const data = reactive<DashboardData>({
    totalProductCount: 0,
    lowStockCount: 0,
    outOfStockCount: 0
})
onMounted(
    async ()=>{
        const response = await axiosInstance.get('/api/dashboard');
        data.lowStockCount =response.data?.lowStockCount
        data.outOfStockCount = response.data?.outOfStockCount
        data.totalProductCount = response.data?.totalProductCount
    }
)
const summaryCards = computed( () => [
    {
        icon: "system-uicons:boxes",
        title: "Total Products",
        value: data.totalProductCount,
        color: "var(--stockley-deep-blue)",
    },
    {
        icon: "fluent:arrow-trending-down-16-filled",
        title: "Low Stock",
        value: data.lowStockCount,
        color: "#F28C28",
    },
    {
        icon: "tabler:cancel" ,
        title: "Out of stock",
        value: data.outOfStockCount,
        color: "#E34234"
    },
    {
        icon: "quill:outbox",
        title: "Total Stock Out",
        value: "12",
        color: "#50C878",
    },
    
]
)
const today = new Date();
const day = ref(today.toDateString())

</script>

<template>
        <div class="greeting">
            <div class="info">
                <p>Hi, User</p>
                <p>Imaginary Trading Enterprise &bull; {{ day }}</p>
            </div>
            <div class="actions">
                <button>Add Product</button>
                <button>Record Stock In</button>
            </div>
        </div>
        <section class="summary">
            <SummaryCard v-for="card in summaryCards" :label = "card.title" :value="card.value" :icon="card.icon" stat="Up 5% from last restock"/>

        </section>
        <section class="quick-actions">
            <h4>Quick Actions</h4>
            <div class="links">
                <RouterLink to="/products">
                    <Icon icon="mingcute:add-fill" width="1.2em" height="1.2em" />
                    Add product
                </RouterLink>
                
                <RouterLink to="/products">
                    <Icon icon="system-uicons:box-add" width="1.2em" height="1.2em" />
                    Restock product
                </RouterLink>
                <RouterLink to="/products">
                    <Icon icon="system-uicons:box-remove" width="1.2em" height="1.2em" />
                    Record stock out
                </RouterLink>
                

            </div>
        </section>
        <section class="tables">
            <RecentStockTable />
            <LowStockProductsTable />
        </section>
    

</template>

<style scoped>
*{
    padding: 0;
    margin: 0;
}
.greeting{
    display: grid;
    grid-template-columns: 3fr 2fr;
    background-image: linear-gradient(135deg, var(--stockley-deep-blue), var(--deep-blue-10),  var(--deep-blue-20));
    padding: 0.8rem 1rem;
    color: var(--grey-80);
    border-radius: 1rem;
    line-height: 1.2rem;
    align-items: center;
}
.info > p:first-child{
    font-size: 1rem;
}
.info > p:last-child{
    font-size: 0.8rem;
}

.actions{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    
}
.actions > button{
    border-radius: 0.8rem;
    padding: 0.5rem 0;
    border: none;
    cursor: pointer;
    
}
.actions button:first-child:hover{
    background-color: var(--white-30);
}
.actions button:last-child:hover{
    background-color: var(--deep-blue-40);
}
.actions > button:first-child{
    border-radius: 0.8rem;
    padding: 0.5rem 1rem;
    background-color: var(--white-10);
    color: var(--deep-blue-10);
}
.actions > button:last-child{
    border-radius: 0.8rem;
    padding: 0.5rem 1rem;
    background-color: #7aa5d0a3;
    color: var(--white-10);
}
section h4 {
    font-weight: 500;
    letter-spacing: -1px;
}
.quick-actions {
    padding: 1rem;
    display: grid;
    grid-template-columns: 1fr 6fr;
   
}
.links{
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(3, 1fr);
    align-items: center;
}
.links a:first-child{
    background-color: var(--deep-blue-10);
    color: var(--white-10);

}
.links a{
    border: 1px solid var(--deep-blue-20);
    color: var(--deep-blue-20);
}

.quick-actions a{
    
    display: inline-flex;
    cursor: pointer;
    border-radius: 1rem;
    text-align: center;
    font-weight: 500;
    letter-spacing: -1px;
    /* justify-content: space-around; */
    gap: 0.5rem;
    padding: 0 1rem;
    align-items: center;
}
.quick-actions a:hover{
    background-color: var(--stockley-deep-blue);
    color: var(--white-10)
}

.summary {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1rem 0;
    
}

.card .value{
    font-size: larger;
    font-weight: 700;
    color: var(--grey-shade-40);
}
a{
    text-decoration: none;
    color: var(--stockley-teal);
}
.tables{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 1rem;
}
@media (max-width: 768px){
    .tables{
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1rem;
    margin: 1rem;
}
    .summary-grid, .actions{
        display: grid;
        grid-template-columns: 1fr;
       
        
    }
}

</style>