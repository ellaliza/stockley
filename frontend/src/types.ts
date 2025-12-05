
import type { DefineComponent } from "vue";

export interface Product {
    productName: string;
    productId: number;
    initialStock: number;
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