import axios from 'axios';
import created_model from "../interfaces/created_model";

const baseURL = '/api';
axios.defaults.withCredentials = true;


const getToken = () =>{
    return localStorage.getItem('access_token')
}

async function getModels() {
    try {
        const token = localStorage.getItem('access_token');  // Get the JWT token from local storage
        const response = await axios.get(`${baseURL}/models`, {
            headers: {
                'Authorization': `Bearer ${token}`  // Add the token to the Authorization header
            },
            withCredentials: true,
        });
        return response.data.models;
    } catch (error) {
        console.error('Error fetching models:', error);
        throw error;
    }
}

async function addModel(model: created_model) {
    try {
        const token = getToken();  // Get the JWT token from local storage
        console.log(token)
        const response = await axios.post(`${baseURL}/models`, model, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${token}`  // Add the token to the Authorization header
            }, 
            withCredentials: true
        });
        
        return response.data;
    } catch (error) {
        console.error('Error adding model:', error);
        throw error;
    }
}

async function login(username: string, password: string) {
    try {
        const response = await axios.post(`${baseURL}/login`, { username, password }, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true
        });

        return { status: response.status, access_token: response.data.access_token };
    } catch (error) {
        console.error('Error logging in:', error);
        throw error;
    }
}


async function register(username: string, email: string, password: string) {
    try {
        const response = await axios.post(`${baseURL}/register`, { username, email, password }, {
            headers: {
                "Content-Type": "application/json",
            }, 
            withCredentials: true
        });
        return { status: response.status };
    } catch (error) {
        console.error('Error registering:', error);
        throw error;
    }
}

async function uploadDataset() {
    // Implementation needed
}

async function deployModel(id: number) {
    try {
        const token = getToken()
        const response = await axios.post(`${baseURL}/models/deploy`, { model_id: id }, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${token}`  // Add the token to the Authorization header
            }, 
            withCredentials: true
        });
        return { status: response.status };
    } catch (error) {
        console.error('Error deploying model:', error);
        throw error;
    }
}

async function forecast(id: number, timeline: number) {
    try {
        const token = getToken()
        const response = await axios.post(`${baseURL}/models/forecast`, { model_id: id, timeline: timeline }, {
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${token}`  // Add the token to the Authorization header
            },
            withCredentials: true, // Ensure that cookies are sent with the request
        });

        const data = await response.data;

        return { status: response.status, predictions: data.predictions, history: data.history };
    } catch (error) {
        console.error('Error forecasting model:', error);
        throw error;
    }
}

export default { getModels, addModel, login, register, uploadDataset, deployModel, forecast };
