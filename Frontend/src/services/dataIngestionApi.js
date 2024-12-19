import axios from 'axios';
import { ApiURL } from '../utils/configurations/apiUrl';


export const getBlobFilesList = () => {

        const response = axios.get(`${ApiURL}/data_ingestion/get_blobs`, {
            withCredentials: true
        });
        return response;
};

export const uploadNewFile = (files, reportDate) => {

    const formData = new FormData();
    files.forEach((file) => {
        formData.append('files', file);
    });
    formData.append("reporting_date", reportDate);

    const response = axios.post(`${ApiURL}/data_ingestion/upload_source`, formData, {
        withCredentials: true
    });
    return response;
};