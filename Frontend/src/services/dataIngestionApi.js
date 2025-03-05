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
	});
	// formData.append("fund_type", selectedFunds);


	const response = axios.post(`${ApiURL}/data_ingestion/upload_source`, formData, {
		withCredentials: true
	});
	return response;
};


export const exportBaseDataFile = (uploadedFilesData, selectedFund) => {
	const uploadedData = {
		"files_list": uploadedFilesData,
		"fund_type": selectedFund
	};
	const exportRes = axios.post(`${ApiURL}/data_ingestion/extract_base_data`, uploadedData);
	return exportRes;
};

export const getBaseFilePreviewData = (info_id) => {
	const fileData = {
		'info_id': info_id
	};
	const previewResponse = axios.post(`${ApiURL}/data_ingestion/get_base_data`, fileData);
	return previewResponse;
};

export const getBaseDataFilesList = (data) => {
	const fileData = {
		"report_date": data.report_date,
		"company_id": data.company_id,
		"fund_type": data.fund_type,
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

export const submitOtherInfo = async (data) => {
	const response = await axios.post(`${ApiURL}/data_ingestion/base_data_other_info`, data);
	return response.data;
};

export const updateSeletedColumns = (columnIds, previewFundType) => {
	const columnData = {
		"selected_col_ids": columnIds,
		"fund_type": previewFundType
	};

	const response = axios.post(`${ApiURL}/data_ingestion/update_bd_col_select`, columnData);
	return response;
};

export const updateColumnsOrder = (updatedOrderData) => {
	const columnData = {
		"updated_sequence": updatedOrderData
	};

	const response = axios.post(`${ApiURL}/data_ingestion/change_bd_col_seq`, columnData);
	return response;
};

export const updateArchiveStatus = (fileIds, addToArchive) => {
	const filesData = {
		"list_of_ids": fileIds,
		"to_archive": addToArchive
	};
	const response = axios.put(`${ApiURL}/data_ingestion/update_archived_files`, filesData);
	return response;
};

export const getArchive = () => {
	const response = axios.get(`${ApiURL}/data_ingestion/get_archived_files`);
	return response;
};

export const getUnmappedSecurityData = (securityType) => {
	const payload = {
		"security_type": securityType
	};
	const fileListResponse = axios.post(`${ApiURL}/data_ingestion/get_cash_securities`, payload);
	return fileListResponse;
};


export const getProbableSecuritiesData = (cashSecurity) => {
	const payload = {
		"cash_file_security": cashSecurity
	};
	const fileListResponse = axios.post(`${ApiURL}/data_ingestion/get_unmapped_pflt_sec`, payload);
	return fileListResponse;
};

export const uploadAddMoreSecFile = (file, dataId, fundType, reportDate) => {
	const formData = new FormData();
	formData.append('base_data_info_id', dataId);
	formData.append('fund_type', fundType);
	formData.append('report_date', reportDate);
	formData.append('file', file); // Append the file

	return axios.post(`${ApiURL}/data_ingestion/add_base_data`, formData, {
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	});
};

