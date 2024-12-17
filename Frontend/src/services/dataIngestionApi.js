import axios from 'axios';
import { ApiURL } from '../utils/configurations/apiUrl';


export const getBlobFilesList = () => {

        const response = axios.get(`${ApiURL}/data_ingestion/get_blobs`, {
            withCredentials: true
        });
        return response;
};