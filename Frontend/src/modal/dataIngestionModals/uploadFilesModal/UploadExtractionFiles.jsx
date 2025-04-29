import { Checkbox, DatePicker, Modal } from 'antd';
import React, { useState } from 'react';
import { ModalComponents } from '../../../components/modalComponents';
import { DynamicFileUploadComponent } from '../../../components/reusableComponents/dynamicFileUploadComponent/DynamicFileUploadComponent';
import { uploadNewFile } from '../../../services/dataIngestionApi';
import { checkboxOptions } from '../../../utils/constants/constants';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './UploadExtractionFiles.module.css';

export const UploadExtractionFiles = ({uploadFilesPopupOpen, setUploadFilesPopupOpen, blobFilesList }) => {

	const [selectedFiles, setSelectedFiles] = useState([]);
	const [loading, setLoading] = useState(false);
	const [reportDate, setReportDate] = useState();
	const [reportDateStr, setReportDateStr] = useState();
	const [selectedOptions, setSelectedOptions] = useState([]);

	const handleCancel = () => {
		setSelectedFiles([]);
		setSelectedOptions([]);
		setUploadFilesPopupOpen(false);
		setReportDate();
	};


	const handleDateChange = (date, dateStr) => {
		setReportDate(date);
		setReportDateStr(dateStr);
	};

	const handleFileUpload = async() => {



		if (!reportDate || reportDate == "") {
			showToast('warning', "Select Report Date");
			return;
		}
		setLoading(true);
		try {
			const selectedFunds = selectedOptions;
			await uploadNewFile(selectedFiles, reportDateStr, selectedFunds);

			// await blobFilesList(selectedOptions);
			showToast('success', "File upload and extraction is in progress, it may take few minutes");
			// showToast('success', uploadresponse?.data?.message);
		} catch (error) {
			showToast('error', error?.response?.data.message);
		} finally {
			await blobFilesList(selectedOptions);
		}
		setSelectedFiles([]);
		setSelectedOptions([]);
		setUploadFilesPopupOpen(false);
		setLoading(false);
	};

	const handleCheckboxChange = (checkedValues) => {
		setSelectedOptions(checkedValues);
	};


	return (
		<>
			<Modal
				title={<ModalComponents.Title title='Upload File(s)' showDescription={true} description='Upload source files for base data extraction' />}
				centered
				open={uploadFilesPopupOpen}
				onCancel={handleCancel}
				width={'70%'}
				footer={<ModalComponents.Footer onClickCancel={handleCancel} onClickSubmit={handleFileUpload} loading={loading} submitText='Load' />}
			>
				<>
					<div>
						<div className={styles.calenderContainer}>
							<DatePicker
								// suffixIcon={<img src={CalendarIcon}/>}
								placeholder='Report Date'
								onChange={handleDateChange}
								allowClear={true}
								value={reportDate}
							/>
							<div style={{ marginTop: '20px', marginBottom: '20px'}}>
								<Checkbox.Group
									options={checkboxOptions}
									value={selectedOptions}
									onChange={handleCheckboxChange}
								/>
							</div>
						</div>
						<DynamicFileUploadComponent
							uploadedFiles={selectedFiles}
							setUploadedFiles={setSelectedFiles}
							supportedFormats={['csv', 'xlsx', 'xlsm']}
							showDownload={false}
						/>
					</div>
				</>

			</Modal>

		</>
	);
};
