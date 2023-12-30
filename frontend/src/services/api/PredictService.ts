import { requestBody, responseBody } from "../../models/predict";
import Axios from "axios";


const backend = import.meta.env.VITE_BACKEND_URL;
const secret_key = import.meta.env.VITE_SECRET_KEY;

Axios.defaults.headers.common["secret-key"] = secret_key;

console.log(backend);
export const predictPapers = async(body: requestBody, model: string):  Promise<responseBody[]> =>{
    try { 
        const response = await Axios.post<responseBody[]>(`${backend}/predict/${model}/`, body);
        return response.data;
    }
    catch (error) {
        console.error(error);
        throw error;
    }
}