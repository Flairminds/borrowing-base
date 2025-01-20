import axios from 'axios';
import { ApiURL } from '../utils/configurations/apiUrl';


export const getBlobFilesList = (fundType) => {
    const payload = {
        fund_type: fundType
    };

    const response = axios.post(`${ApiURL}/data_ingestion/get_blobs`, payload, {
        withCredentials: true
    });
    return response;
};

export const uploadNewFile = (files, reportDate, selectedFunds) => {

    const formData = new FormData();
    files.forEach((file) => {
        formData.append('files', file);
    });
    formData.append("reporting_date", reportDate);
    selectedFunds.forEach((fund) => {
        formData.append('fund_type', fund);
    })
    // formData.append("fund_type", selectedFunds);


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

export const getSecurityMappingData = () => {
    const fileListResponse = axios.get(`${ApiURL}/data_ingestion/get_pflt_sec_mapping`);
    return fileListResponse;
};

export const editPfltSecMapping = (changes) => {
    const payload = { changes };
    const response = axios.post(`${ApiURL}/data_ingestion/edit_pflt_sec_mapping`, payload);
    return response;
};

export const postSourceFileData = (payload) => {
    return axios.post(`${ApiURL}/data_ingestion/get_source_file_data`, payload);
};

export const postAddSecurityMapping = (payload) => {
    return axios.post(`${ApiURL}/data_ingestion/add_sec_mapping`, payload);
};

export const editBaseData = (changes) => {
    const payload = { changes };
    const response = axios.post(`${ApiURL}/data_ingestion/edit_base_data`, payload);
    return response;
};