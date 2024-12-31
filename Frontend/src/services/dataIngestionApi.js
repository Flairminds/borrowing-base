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

export const exportBaseDataFile = (uploadedFilesData) => {
    const uploadedData = {
        "files_list": uploadedFilesData
    };
    const exportRes = axios.post(`${ApiURL}/data_ingestion/extract_base_data`, uploadedData);
    return exportRes;
};

export const getBaseFilePreviewData = (info_id) => {
    const fileData = {
        'info_id': info_id,
    };
    const previewResponse = axios.post(`${ApiURL}/data_ingestion/get_base_data`, fileData);
    return previewResponse;
};

export const getBaseDataFilesList = (data) => {
    const fileData = {
        "report_date": data.report_date,
        "company_id": data.company_id,
        "extracted_base_data_status_id": data.id
    };
    const fileListResponse = axios.post(`${ApiURL}/data_ingestion/get_extracted_base_data_info`, fileData);
    return fileListResponse;
};