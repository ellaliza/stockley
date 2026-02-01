<script lang="ts" setup>
import { type JSX } from 'vue/jsx-runtime';
const getStatusClass = (value: number): string => {
    return value === 0 ? "out-of-stock" : value === 1 ? "low-stock" : "in-stock"
}
</script>

<template>
    <div class="table">
        <h4>Low Stock Products</h4>
        <small>Across all stores</small>
        <table>
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Status</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Milo 30g</td>
                    <td>
                        <p :class="getStatusClass(0)">
                            Out of Stock
                        </p>
                    </td>
                    <td>5</td>
                </tr>
                <tr>
                    <td>Awake Water 750ml</td>
                    <td>
                        <p :class="getStatusClass(1)">
                            Low Stock
                        </p>
                    </td>
                    <td>5</td>
                </tr>
                <tr>
                    <td>Verna Water 500ml</td>
                    <td>
                        <p :class="getStatusClass(2)">
                            In Stock
                        </p>
                    </td>
                    <td>5</td>
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
    thead tr{
        color: var(--grey-10);
        font-size: small;
        background-color: var(--grey-80);
        border-top-left-radius: 0.5rem;
        border-top-right-radius: 0.5rem;
        
    }
    thead th:first-child{
        border-top-left-radius: 0.5rem;
    }
    thead th:last-child{
        border-top-right-radius: 0.5rem;
    }
    tbody{
        color: var(--grey-shade-40);
        font-size: 0.85rem;
    }
    th, td{
        padding: 0.5rem;
        text-align: left;
    }

    table{
        margin-top: 1rem;
        border-collapse: collapse;
        width: 100%;
        border-radius: 0.5rem;
        letter-spacing: -1px;
        font-size: 12px;
    }
    tbody > tr > td:nth-child(2n){
        color: var(--white-30);
        min-width: 4.5rem;
        align-items: center;
        
        gap: 0.55rem;
        font-size: 10px;
    }
    td:nth-child(2n) > p{
        padding: 0.1rem 0.5rem;
        display: inline;
        border-radius: 1rem;
    }
    h4{
        font-weight: 500;
    }
    small{
        font-weight: 500;
        font-size: 11px;
        line-height: 1;
    }
    .table{
        background-color: var(--white-10);
        box-shadow:  0.05rem 0.05rem 0.4rem var(--grey-60);
        padding: 1rem;
        border-radius: 0.7rem;
    }
    tbody tr{
        vertical-align: middle;
    }

</style>