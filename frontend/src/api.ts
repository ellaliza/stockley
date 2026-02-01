import axios from "axios";

export const axiosInstance = axios.create({
    baseURL: "https://backend.ellaliza.dev",
    headers: {
        "Content-Type": "application/json",
        
    }
})