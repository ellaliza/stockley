import axios from "axios";

export const axiosInstance = axios.create({
    baseURL: "https://mallie-lacklustre-deadra.ngrok-free.dev",
    headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": true,
    }
})