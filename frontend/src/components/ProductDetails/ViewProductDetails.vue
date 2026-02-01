<script setup lang="ts">
import type { Product } from '@/types';
import { ref } from 'vue';

const locations = ["Accra Newtown", "New Gbawe Zero", "Gbawe CP", "Ablekuma NIC"]
const props = defineProps<{product: Product}>()

const product = ref<Product>(props.product)
</script>

<template>
<div class="columns">
    <div>
        <h4>Product Details</h4>
        <div>
            <div class="product-detail-field">
                <p>Name</p>
                <p>{{ product.productName }}</p>
            </div>
            <div class="product-detail-field">
                <p>Category</p>
                <p>Groceries</p>
            </div>
            <div class="product-detail-field">
                <p>Supplier</p>
                <p>Atona Foods</p>
            </div>
            <div class="product-detail-field">
                <p>Cost Price</p>
                <p>GH&#x20B5; 20.00</p>
            </div>
            <div class="product-detail-field">
                <p>Product ID</p>
                <p>{{ product.productId }}</p>
            </div>

        </div>
    </div>
    <div style="display: flex; flex-direction: column;">
        <h4>Stock Details</h4>
        <div class="location-select">
            <label for="location">Location</label>

            <select name="location">
                <option v-for="location in locations" :value="location">{{ location }}</option>
            </select>
        </div>
        <div class="stock-detail-field">
            <p>Initial Stock</p>
            <p>{{ product.initialStock }}</p>
        </div>
        <div class="stock-detail-field">
            <p>Current Stock</p>
            <p>{{ product.currentStock }}</p>
        </div>
        <div class="stock-detail-field">
            <p>{{ product.minimumStockLevel }}</p>
            <p>25</p>
        </div>
        <div class="stock-detail-field">
            <p>Available Stock</p>
            <p>80</p>
        </div>
        <div class="stock-detail-field">
            <p>Reserved Stock</p>
            <p>0</p>
        </div>
        <div class="stock-detail-field">
            <p>Last Activity</p>
            <p>
                Stock In &bull; 20pcs <br/> 
                by Ella &bull; 2 days ago
            </p>
        </div>
    </div>
    

</div>
</template>

<style lang="css" scoped>
.columns{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}
.product-detail-field > p:first-child, .stock-detail-field > p:first-child{
    color: var(--grey-10);
    font-size: 0.7rem;
    font-weight: 500;
}
.product-detail-field{
    line-height: 1.2rem;
    padding: 0.3rem 0;
}
.stock-detail-field, .location-select{
display: flex;
justify-content: space-between;
padding: 0.2rem 0;
align-items: center;
flex-grow: 1;
}
h4{
    color: black;
    font-weight: 500;
}
</style>