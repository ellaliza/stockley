<script setup lang="ts">
import type { Product } from '@/types';
import { reactive, ref } from 'vue';
const emit = defineEmits<{
    (e: 'change', newDetails: Product) : void,
}>()
const locations = ["Accra Newtown", "New Gbawe Zero", "Gbawe CP", "Ablekuma NIC"]
const props = defineProps<{product: Product}>()

const product = reactive<Product>({...props.product});

const makeChanges = () => {
    console.log(product.productName)
    emit('change', {...product});
}
</script>

<template>
<div class="columns">
    <div>
        <h4>Product Details</h4>
        <div>
            <div class="product-detail-field">
                <p>Name</p>
                <input type="text" v-model="product.productName" @change="makeChanges"/>
                
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
            <input type="number" v-model="product.initialStock" />
            
        </div>
        <div class="stock-detail-field">
            <p>Current Stock</p>
             <input type="number" v-model="product.currentStock" />
            
        </div>
        <div class="stock-detail-field">
            <p>Minimum Stock Level</p>
            <input type="number" v-model="product.minimumStockLevel" />
            
            
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

input, select{
    border: 1px solid var(--grey-40);
    padding: 0.3rem 0.3rem;
    border-radius: 0.4rem;
}
input[type='number']{
    width: 5rem;
}
input:focus{
    outline: none;
}
</style>