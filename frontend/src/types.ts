
import type { DefineComponent } from "vue";

export interface Product {
    productName: string;
    productId: number;
    initialStock: number;
    currentStock: number;
    minimumStockLevel?: number;
    status?: number;
    statusText?: string;
}

//export type NewProduct = Omit<Product, "initialStock" | "productId" >
export interface NewProduct {
    productName: string;
    currentStock: number;
    minimumStockLevel?: number;
}

export interface route {
    path: string;
    component: DefineComponent<{}, {}, any>;
 }

export interface DashboardData {
    
    totalProductCount: number,
    lowStockCount: number,
    outOfStockCount: number

}

export interface StockFilter {
    label: string,
    value: 0 | 1 | 2;
}

export type ProductModalMode = "view" | "edit" | "restock" | "stockOut";