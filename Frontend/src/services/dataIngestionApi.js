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
        "master_comp_file_id": uploadedFilesData[0],
        "cash_file_id": uploadedFilesData[1]
        // "SOI_id": uploadedFilesData[2]
    };
    const exportRes = axios.post(`${ApiURL}/data_ingestion/extract_base_data`, uploadedData);
    return exportRes;
};

export const getBaseFilePreviewData = (reportDate, companyId) => {
    const fileData = {
        'report_date': reportDate,
        'company_id': companyId
    };
    const previewResponse = axios.post(`${ApiURL}/data_ingestion/get_base_data`, fileData);
    return previewResponse;
};

export const getBaseDataFilesList = (data) => {
    const fileData = {
        "report_date": data.reportDate,
        "company_id": data.companyId,
        "extracted_base_data_status_id": data.baseFileId
    };
    const fileListResponse = axios.post(`${ApiURL}/data_ingestion/get_extracted_files_list`, fileData);
    return fileListResponse;
};