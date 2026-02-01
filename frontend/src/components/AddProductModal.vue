<script setup lang="ts">
import { computed, reactive } from 'vue';
import type { NewProduct } from '@/types';

const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'addProduct', product: NewProduct): void,
}>()

const newProduct = reactive<NewProduct>({
    productName: "",
    currentStock: 0,
    minimumStockLevel: 0
})

</script>
<template>
    <div class="modal-background">
        <div class="modal">
            <h3>Add Product</h3>
            <small>Add a new product to the digital inventory </small>

            <section class="section basic-info">
                <h5>Basic Info</h5>
                <small>Basic information about the product</small>
                <div class="form">
                    <div>
                        <label for="product-name">Product Name</label>
                        <input type="text" name="product-name" v-model="newProduct.productName"/>
                    </div>
                </div>

            </section>
            <section class="section inventory">
                <h5>Inventory</h5>
                <small>Track your product's stock and when to order</small>
                <div class="form">
                    <div>
                        <label for="current-stock">Current Stock</label>
                        <input type="number" name="current-stock" v-model="newProduct.currentStock" />
                    </div>
                    
                    <div>
                        <label for="min-stock-level">Minimum Stock Level</label>
                        <input type="number" name="min-stock-level" v-model="newProduct.minimumStockLevel"/>
                    </div>
                </div>

            </section>
            <section class="footer">
                <small>All fields can be updated later.</small>
                <div>
                    <button class="cancel" @click="emit('close')">Cancel</button>
                    <button class="save" @click="emit('addProduct', newProduct)">Save</button>
                </div>
            </section>
        </div>
    </div>
</template>
<style scoped>
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
    }
    small{
        font-weight: 400;
        line-height: 1;
        
    }
    h4, h5{
        line-height: 1;
    }
    .form{
        display: grid;
        grid-template-columns: 1fr 1fr;
        margin: 0.4rem 0;
        gap: 1rem;

    }
    .form > div{
        display: grid;
    }
    section{
        margin-top: 2rem;
    }
    label{
        font-size: 11px;
    }
    input:focus{
        outline: none;
    }
    input{
        padding: 0.1rem 0.2rem;
        border-radius: 0.3rem;
        border: 1px solid var(--grey-60);
    }
    .footer > div{
        float: right;
        display: grid;
        grid-template-columns: 1fr 1fr ;
        gap: 1rem;
    }
    .footer button{
        font-size: 11px;
        padding: 0.2rem 0.8rem;
        border: none;
        cursor: pointer;
        border-radius: 0.5rem;
    }
    button.save{
        background-color: var(--stockley-deep-blue);
        color: var(--white-10);

    }
    button.cancel{
        background-color: var(--grey-40);
        color: var(--grey-shade-40)

    }

</style>