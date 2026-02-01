<script lang="ts" setup>
import type { Product } from '@/types';
import { computed } from 'vue';
import { Icon } from '@iconify/vue';
const props = defineProps<{
  products: Product[]
}>()
const emit = defineEmits<{
    (e: "refresh"): void,
    (e: "productClick", productId: number) : void,
}>()
const getStatusClass = (value: number): string => {
    return value === 0 ? "out-of-stock" : value === 1 ? "low-stock" : "in-stock"
}

// const products: Product[] = props.products;
const productStatus = ["Out of Stock", "Low Stock", "In Stock"];
const productList = computed(()=>{
    console.log(props.products)
    if (Array.isArray(props.products)){
        
        return props.products.map(
            (product, index) => {
                const status = product.currentStock <= product.minimumStockLevel ? (product.currentStock === 0 ? 0 : 1) : 2;
                product.status = status;
                product.statusText = productStatus[status];
                return product;
            }
        )
    }
    else {return []}
})


</script>

<template>
    <div class="table-container">
        <div class="header-content">
            <small>Showing {{productList.length}} of {{ productList.length }} products</small>
            <div class="refresh" @click="emit('refresh')">
                <Icon icon="mynaui:refresh-alt" width="1.2em" height="1.2em" />
            </div>
            
        </div>
        <table>
            <thead>
                <tr>
                    <th>
                        <input type="checkbox"/>
                    </th>
                    <th>Product</th>
                    <th>ID</th>
                    <th>Current Stock</th>
                    <th>Min Stock Level</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in productList" @click="emit('productClick', item.productId)">
                    <td>
                        <input type="checkbox" />
                    </td>
                    <td>{{ item.productName }}</td>
                    <td>{{ item.productId }}</td>
                    <td>{{ item.currentStock }}</td>
                    <td>{{item.minimumStockLevel}}</td>
                    <td >
                       <p :class="getStatusClass(item.status)">{{item.statusText}}</p> 
                    </td>       
                </tr>
                
            </tbody>
        </table>
    </div>
</template>
<style scoped>
    .low-stock{
        background-color: #ed6c02;
    }
    .out-of-stock{
        background-color: #ef5350;
    }
    .in-stock{
        background-color: #2e7d32;
    }
    .table-container{
        background-color: white;
        border-radius: 1rem;
        box-shadow: 1px 1px 10px var(--grey-80);
        padding-bottom: 0.5rem;
        margin-top: 3rem;
    }
    table{
        width: 100%;
        text-align: left;
        border-collapse: collapse;
        font-size: 12px;
        
    }
    thead{
        background-color: var(--grey-80);
    }
    table td:first-child, table th:first-child, table td:last-child, table th:last-child {
        padding: 0rem 0.8rem;
    }
    input[type="checkbox"]{
        border: none;
        user-select: none;
    }
    .header-content{
        padding: 0.5rem 1rem;

    }
    tr > td:last-child > p{
        color: white;
        padding: 0.1rem 0.5rem;
        display: inline;
        border-radius: 1rem;
        font-size: 12px;
    }
    tr, td{
        padding: 0.5rem 0;
    }
    .refresh{
        float: right;
        cursor: pointer;
    }
    .refresh:hover{
        color: var(--grey-40);
    }
</style>