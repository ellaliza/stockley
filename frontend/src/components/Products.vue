<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
import type { Product } from '../types';

import { axiosInstance } from '@/api';


const productId = ref<string>("");
const products = ref<Product[]>();
const product = ref<Product>()
const newStock = ref<number>()
const quantityToSell = ref<number>()

const newProduct = reactive<Product>({
    productId: 0,
    productName: "",
    initialStock: 0,
    currentStock: 0
})

const getProduct = async () => {
    const response = await axiosInstance.get(`/products/${productId.value}`);
    console.log(response.data);
    product.value = response.data
}
const createProduct = async ()=>{
    if (
    !newProduct.productId ||
    newProduct.productName.trim() === "" ||
    newProduct.initialStock === null ||
    newProduct.currentStock === null
) {
    alert("Please fill all details!")
    return
}


    const response = await axiosInstance.post('/products/', newProduct);
    if (response.status === 200 || response.status === 201){
        alert("created");
        newProduct.productName = ""
        newProduct.currentStock = 0;
        newProduct.initialStock = 0;
        newProduct.productId = 0;
    }
}
const restockProduct = async () => {
    getProduct();
    console.log(newStock.value)
    if (newStock.value && newStock?.value <= 0 || !newStock.value){
        alert("Added stock must be greater than 0");
        return
    }
    const response = await axiosInstance.get('/products/restock/'+productId.value, {params: {quantity: newStock.value}});
    alert("success!")
    getProduct();
    newStock.value = 0

}
const stockOutProduct = async () => {
    getProduct();
    console.log(quantityToSell.value)
    if (quantityToSell.value && quantityToSell?.value <= 0 || !quantityToSell.value){
        alert("Quantity stocked out must be more than 0");
        return
    }
    const response = await axiosInstance.get('/products/stock-out/'+productId.value, {params: {quantity: quantityToSell.value}});
    alert("success!")
    getProduct();
    quantityToSell.value = 0
}
const getProducts = async () => {
    const response = await axiosInstance.get(`/products/`);
    products.value = response.data
}
</script>

<template>
    <h1>Products</h1>
    <div class="action">
        <h3>View a product</h3>
        <div class="field">
            <span>Product ID:</span> 
            <input type="text" v-model="productId"></input>
        </div><br />
        <button @click="getProduct()">Finish</button><br /><br />
        <div v-if="product" class="table-head">
            <p>Product Id</p>
            <p>Product Name</p>
            <p>Initial Stock</p>
            <p>Current Stock</p>
        </div>
        <div v-if="product" class="table-row">
            <p>{{ product.productId }}</p>
            <p>{{ product.productName}}</p>
            <p>{{ product.initialStock}}</p>
            <p>{{product.currentStock}}</p>
        </div>
        
    </div>
    <div class="action">
        <h3>Add a product</h3>
        <div class="field">
            <span>Product ID:</span> 
            <input type="number" v-model="newProduct.productId"/>
        </div>
        <div class="field">
            <span>Product Name:</span> 
            <input type="text" v-model="newProduct.productName"></input>
        </div>
        <div class="field">
            <span>Initial Stock:</span> 
            <input type="number" v-model="newProduct.initialStock"></input>
        </div>
        <div class="field">
            <span>Current Stock:</span> 
            <input type="text" v-model="newProduct.currentStock"></input>
        </div>
        </br>
        <button @click="createProduct()">Finish</button><br /><br />
    </div>
    <div class="action">
        <h3>Restock product</h3>
        <div class="field">
            <p style="grid-column: 1/ span 2;">Enter product id to fetch details</p>
            <span>Product ID:</span> 
            <input type="number" v-model="productId"/>
        </div>
        <div class="field">
            <span>Product Name:</span> 
            <input type="text" :value="product && product.productName" disabled></input>
        </div>
        <div class="field">
            <span>Current Stock:</span> 
            <input type="number" :value="product && product.currentStock" disabled/>
        </div>
        <div class="field">
            <span>New Stock:</span> 
            <input type="number" v-model="newStock"></input>
        </div>
        </br>
        <button @click="restockProduct()">Finish</button><br /><br />
    </div>
    <div class="action">
        <h3>Sell product</h3>
        <div class="field">
            <p style="grid-column: 1/ span 2;">Enter product id to fetch details</p>
            <span>Product ID:</span> 
            <input type="number" v-model="productId"/>
        </div>
        <div class="field">
            <span>Product Name:</span> 
            <input type="text" :value="product && product.productName" disabled></input>
        </div>
        <div class="field">
            <span>Current Stock:</span> 
            <input type="number" :value="product && product.currentStock" disabled/>
        </div>
        <div class="field">
            <span>Quantity:</span> 
            <input type="number" v-model="quantityToSell"></input>
        </div>
        </br>
        <button @click="stockOutProduct()">Finish</button><br /><br />
    </div>
    <div class="action">
        <h3>Sell Products</h3>
        <button @click="getProducts()">Fetch all</button><br /><br />

        <div v-if="products">
            <div v-for="prod in products">
                <span v-for="key of prod">{{ key + " "}}</span>
            </div>
            
        </div>
        
    </div>
</template>

<style scoped>
.field {
    display: grid;
    grid-template-columns: 1fr 3fr;
    padding: 0.5rem 0;
}
.action{
    padding: 1rem;
    border: 1px solid cadetblue;
    margin: 0.5rem 0;
}
.action > button{
    content: "Finish";
    border: 1px solid;
    padding: 0.3rem;
    border-radius: 0.5rem;
    cursor: pointer;
    background-color: cadetblue;
    
}
.table-head > p {
    font-weight: bold;
}
.table-head, .table-row{
    display: grid;
    grid-template-columns: 1fr 3fr 1fr 1fr;
    gap: 0.5rem;
    border-bottom: solid 1px ;
    }

.table-head > p:not(:last-child), .table-row > p:not(:last-child){
    border-right: solid 1px black;
}
</style>