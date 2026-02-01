<script lang="ts" setup>
import { type JSX } from 'vue/jsx-runtime';
const getActionClass = (value: string): string => {
    return value === "Stock In" ? "stock-in" : "stock-out"
}
</script>

<template>
    <div class="table">
        <h4>Recent Stock Activity</h4>
        <small>Last 24 hours</small>
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Product Name</th>
                    <th>Action</th>
                    <th>Quantity</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>9:20</td>
                    <td>Milo 30g</td>
                    <td>
                        <p :class="getActionClass('Stock In')">
                            Stock In
                        </p>
                    </td>
                    <td>5</td>
                </tr><tr>
                    <td>10:30</td>
                    <td>Milo 30g</td>
                    <td>
                        <p :class="getActionClass('Stock Out')">
                            Stock Out
                        </p>
                    </td>
                    <td>5</td>
                </tr>

            </tbody>
        </table>

    </div>
</template>

<style scoped>
    .stock-in{
        background-color: var(--teal-shade-10);
    }
    .stock-out{
        background-color: var(--stockley-deep-blue);
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
    tbody > tr > td:nth-child(3n){
        color: var(--white-30);
        min-width: 4.5rem;
        align-items: center;
        
        gap: 0.55rem;
        font-size: 10px;
    }
    td:nth-child(3n) > p{
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