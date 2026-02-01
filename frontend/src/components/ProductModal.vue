<script setup lang="ts">
import type { ProductModalMode, Product } from '@/types';
import { onMounted, ref } from 'vue';
import ViewProductDetails from '@/components/ProductDetails/ViewProductDetails.vue';
import EditProductDetails from './ProductDetails/EditProductDetails.vue';

const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'update', prod: Product) : void,
}>()
const mode = ref<ProductModalMode>("view")
const modes = {
    view: "View all details about a product",
    edit: "Make changes to product details",
    restock: "Record stock in for particular product",
    stockOut: "Record sale or stock out for product"
}
const props = defineProps<{product: Product}>()
const product = ref<Product>(props.product)
const updatedProduct = ref<Product>(props.product)

const switchMode = (newMode : ProductModalMode) => {
    mode.value = newMode;
}
const handleProductEdit = (prod: Product) => {
    updatedProduct.value = prod;
    

}
</script>

<template>
    <div class="modal-background">    
        <div class="modal">
            <h3>{{ product.productName }}</h3>
            <small>SKU: SI-2390-GB &bull; Category: Groceries &bull; Location: Gbawe</small>
            <div class="info">
                <div class="mode-options">
                    <p class="mode" :class="{ 'active-mode': mode === 'view' }" @click="switchMode('view')">View</p>
                    <p class="mode" :class="{ 'active-mode': mode === 'edit' }" @click="switchMode('edit')">Edit</p>
                    <p class="mode" :class="{ 'active-mode': mode === 'restock' }" @click="switchMode('restock')">Restock</p>
                    <p class="mode" :class="{ 'active-mode': mode === 'stockOut' }" @click="switchMode('stockOut')">Stock Out</p> 
                </div>
                <p class="description">&#x1F6C8; {{ modes[mode] }}</p>
            </div>
            <div class="mode-body">
                
                <ViewProductDetails v-if="mode === 'view'" :product="product"/>
                <EditProductDetails v-if="mode === 'edit'" :product="product" @change="handleProductEdit"/>

            </div>
            <div class="action-button">
                <button class="close-button" @click="emit('close')">Close</button>
                <button class="save-button" @click="emit('update', updatedProduct)" v-if="mode != 'view'">Save Changes</button>
                
                
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
    .mode-options{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.3rem;
        padding: 0.8rem 0;
        align-items: center;
    }
    
    .mode{
        color: var(--grey-10);
        text-align: center;
        padding: 0.1rem 0.2rem;

    }
    .active-mode{
        color: white;
        background-color: var(--stockley-deep-blue);
        border-radius: 0.8rem;
    }
    .modal-background{
        position: fixed;
        top: 0rem;
        left: 0rem;
        background-color: #525050de;
        min-width: 100svw;
        min-height: 100svh;
        display: flex;
        font-size: 13px;
        align-items: center;
        
    }
    .modal{
        margin: auto;
        background-color: var(--white-10);
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 2px 2px 6px var(--grey-10);
        min-width: 30rem;
    }
    .info{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .description{
        color: var(--grey-20);
        font-size: small;
    }
    .close-button{
        background-color: var(--grey-10);
        
    }
    .save-button{
        background-color: var(--stockley-deep-blue);
    }
    .action-button > button{
        border: 0;
        padding: 0.4rem 0.8rem;
        color: white;
        border-radius: 0.5rem;
        
        cursor: pointer;
    }
    .close-button:hover{
        background-color: var(--grey-20);
    }

    .action-button{
        margin-top: 2rem;
        float: right;
        display: flex;
        gap: 1rem;

    }

    @media screen and (max-width: 768px) {
        .info{
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: start;
            margin-bottom: 2rem;
        }
    }

</style>