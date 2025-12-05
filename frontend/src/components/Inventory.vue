<script setup>
</script>

<template>
    <h1>Inventory</h1>
    <div class="action">
        <h3>View product stock</h3>
        <div class="field">
            <span>Product ID:</span> 
            <input type="text"></input>
        </div>
    </div>
    <div class="action">
        <h3>Sell product</h3>
        <div class="field">
            <span>Product ID:</span> 
            <input type="text"></input>
        </div>
        <div class="field">
            <span>Quantity:</span> 
            <input type="number"></input>
        </div>
    </div>
    <div class="action">
        <h3>Restock product</h3>
        <div class="field">
            <span>Product ID:</span> 
            <input type="text"></input>
        </div>
        <div class="field">
            <span>Quantity:</span> 
            <input type="number"></input>
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
</style>