<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { Icon } from '@iconify/vue';
import type { DashboardData } from '../types';
import { axiosInstance } from '@/api';
import { computed, onMounted, reactive, ref } from 'vue';

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

</script>

<template>
        <section class="summary">
            
            <div class="summary-grid">
                <h4 style="grid-column: 1/-1;">Summary</h4>
                <div v-for="card in summaryCards" class="card">
                    <div class="card-title">
                        <p><Icon :icon="card.icon" width="24" height="24" color="var(--teal-shade-40)"/></p>
                        <p>{{card.title}}</p>
                    </div>
                        <p class="value">{{ card.value }}</p>
                </div>
            </div>

        </section>
        <section class="quick-actions">
            <h4>Quick Actions</h4>
            <div class="actions">
                <RouterLink to="/products">Add a new product</RouterLink>
                <RouterLink to="/products">Get product</RouterLink>
                <RouterLink to="/products">Restock product</RouterLink>
                <RouterLink to="/products">Sell product</RouterLink>
                <RouterLink to="/inventory">View Stock</RouterLink>

            </div>
        </section>
        <section class="tables">
            <div>
                <h4>Low Stock Products</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Product ID</th>
                            <th>Product Name</th>
                            <th>Current Stock</th>
                            <th>Minimum Stock</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>3849</td>
                            <td>Milo 30g</td>
                            <td>2</td>
                            <td>5</td>
                        </tr><tr>
                            <td>3849</td>
                            <td>Milo 30g</td>
                            <td>2</td>
                            <td>5</td>
                        </tr>

                    </tbody>
                </table>

            </div>
            <div>

            </div>
        </section>
    

</template>

<style scoped>
section h4 {
    font-weight: 500;
    letter-spacing: -1px;
}
.quick-actions {
    background-color: var(--white-10);
    margin: 1rem;
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0.05rem 0.05rem 0.4rem var(--grey-40);
}
.quick-actions a{
    border: solid 1px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 1rem;
    text-align: center;
    font-weight: 700;
    letter-spacing: -1px;
}
.quick-actions a:hover{
    background-color: var(--grey-80);
}
.actions{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1rem;
}
.summary-grid {
    background-color: var(--white-10);
    border-radius: 1rem;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    padding: 1rem;
    margin: 1rem;
    box-shadow: 0.05rem 0.05rem 0.4rem var(--grey-40);
}
.card{
    padding: 1rem;
    /* background-color: var(--deep-blue-80); */
    border-radius: 0.5rem;
    color: var(--grey-shade-20);
    border: 1px solid var(--grey-40)
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
.tables > div{
    background-color: var(--white-10);
    
    border-radius: 1rem;
    box-shadow: 0.05rem 0.05rem 0.4rem var(--grey-40);   
}
.tables h4{
    padding: 0.8rem 1rem;
}
thead{
    color: var(--grey-10);
    font-size: small;
}
tbody{
    color: var(--grey-shade-10);
    font-size: 0.85rem;
}
th, td{
    padding: 0.5rem
}
thead tr, tr:not(:last-child){
    border-bottom: 1px solid var(--grey-10);
}
table{
    border-collapse: collapse;
    width: 100%;
}
</style>