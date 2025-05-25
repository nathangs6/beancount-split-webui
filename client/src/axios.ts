import axios from "axios";
const apiURL = import.meta.env.VITE_API_URL || "http://localhost:8000/";

const apiClient = axios.create({
    baseURL: apiURL,
    headers: {
        "Content-Type": "application/json",
    }
});

export default apiClient;
