<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
import type { Product, StockFilter } from '@/types';
import { axiosInstance } from '@/api';
import { Icon } from '@iconify/vue';
import ProductListTable from '@/components/ProductListTable.vue';
import AddProductModal from '@/components/AddProductModal.vue';
import type { NewProduct } from '@/types';
import ProductModal from '@/components/ProductModal.vue';


const stockStatusFilters:StockFilter[] = [
    {
        label: "In Stock",
        value: 2
    },
    {
        label: "Low Stock",
        value: 1
    },
    {
        label: "Out of Stock",
        value: 0
    },
]

const stockSortOptions:StockFilter[] = [
    {
        label: "Product Name",
        value: "productName"
    },
    {
        label: "Current Stock",
        value: "currentStock"
    },
    {
        label: "Product ID",
        value: "productId"
    },
]
const emit = defineEmits<{
  (e: 'emitPageTitle', value: string): void
}>()
onMounted(
    () => {
        emit('emitPageTitle', "Products");
        getProducts();
    }
)

const showAddProductModal = ref<boolean>(false)
const showProductModal = ref<boolean>(false)
// --------------------------------------------------
const productId = ref<string>("");
const products = ref<Product[]>();
const product = ref<Product>()
const newStock = ref<number>()
const quantityToSell = ref<number>()


const getProduct = async () => {
    const response = await axiosInstance.get(`/products/${productId.value}`);
    console.log(response.data);
    product.value = response.data
}
const createProduct = async (newProduct: NewProduct)=>{
    if (
    newProduct.productName.trim() === "" ||
    newProduct.minimumStockLevel === null ||
    newProduct.currentStock === null
) {
    alert("Please fill all details!")
    return
}
    let product = {...newProduct, initialStock: newProduct.currentStock}
    
    const response = await axiosInstance.post('/products/', product);
    if (response.status === 200 || response.status === 201){
        
        newProduct.productName = "";
        newProduct.currentStock = 0;
        newProduct.productId = 0;
        showAddProductModal.value = false;
        getProducts()

    }
}
const restockProduct = async () => {
    getProduct();
    console.log(newStock.value)
    if (newStock.value && newStock?.value <= 0 || !newStock.value){
        alert("Added stock must be greater than 0");
        return
    }
    const response = await axiosInstance.post('/products/restock/'+productId.value, {params: {quantity: newStock.value}});
    getProducts();
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
    console.log(products.value)
}
const handleProductUpdate = async (updatedProduct: Product) => {
    try{
        productId.value = updatedProduct.productId
        newStock.value = 20
        restockProduct()
    }catch(error){
        console.log("An error occured: ", error)
    }
}
const showProduct = async (productId: number) => {
    showProductModal.value = true;
    const selectedProduct = products.value?.filter(prod => prod.productId === productId)[0]
    product.value = selectedProduct;
}
</script>

<template>
    <h1>Products</h1>
    <small>Manage your catalog, stock levels and alerts </small>
    <div class="filter-search">
        <div class="search">
            <Icon icon="iconamoon:search-light" width="1.2em" height="1.2em" style="color: var(--grey-10);" />
            <input type="text" class="search-input" placeholder="Search for a product"/>
        </div>
        <div class="filters"> 
    
            <div class="select-container">
                <select name="status-filter">
                    <option value="all" name="status-filter">Filter By</option>
                    <option v-for="filter in stockStatusFilters" :value="filter.value" name="status-filter">{{ filter.label }}</option>
                </select>
            </div>
            
            
        </div>
        <div class="sort">
            
            <div class="select-container">
                <select name="sort">
                    <option value="none" name="sort">Sort By</option>
                    <option v-for="value in stockSortOptions" :value="value.value" name="sort">{{ value.label }}</option>
                </select>
            </div>
        </div>
        
    </div>
    <div class="action">
        <button @click="showAddProductModal = true">
            <Icon icon="mingcute:add-fill" width="1.2em" height="1.2em" /><span>Add Product</span> 
        </button>
    </div>
    <div v-if="Array.isArray(products)">
        <ProductListTable 
        :products="products" 
        @refresh="getProducts"
        @productClick="showProduct"
        />
    </div>
    <AddProductModal 
    :show="showAddProductModal" 
    v-if="showAddProductModal" 
    @close="showAddProductModal = false"
    @addProduct="createProduct"
    />
    <ProductModal 
    :show="showProductModal" 
    v-if="showProductModal"
    @close="showProductModal = false"
    :product="product"
    @update="handleProductUpdate"

    />
    <!-- <div class="action">
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
        
    </div> -->
</template>

<style scoped>
.field {
    display: grid;
    grid-template-columns: 1fr 3fr;
    padding: 0.5rem 0;
}
.action{
   margin-bottom: rem;
}
.action > button{
    padding: 0.3rem 0.6rem;
    border-radius: 0.5rem;
    cursor: pointer;
    border: none;
    background-color: var(--stockley-deep-blue);
    color: var(--white-30);
    vertical-align: middle;
    display: grid;
    align-items: center;
    grid-template-columns: 1fr auto;
    gap: 0.3rem;
    float: right;
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
/* ------------------------- */
.filter-search{
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 2rem;
}
.search{
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid var(--grey-40);
    border-radius: 0.5rem;
    padding: 0.5rem;
}
.search-input{
    border: none;
    flex-grow: 1;
    background-color: inherit;
    color: var(--grey-shade-40);
}
.search-input:focus, .filter-search select:focus{
    outline: none;
}
small{
    font-weight: 500;
}
.filters, .sort{
    display: grid;
}
.filter-search select{
    border: none;
    background-color: inherit;
    width: 100%;
    color: var(--grey-shade-40);
}
.filter-search .select-container{
    /* border: 1px solid var(--grey-40); */
    padding: 0.2rem 0.5rem;
    border-radius: 0.5rem;
}
.filter-search{
    padding: 1rem 0;
}
</style>