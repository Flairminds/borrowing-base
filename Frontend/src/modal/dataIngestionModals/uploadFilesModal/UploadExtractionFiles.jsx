import { Button, Checkbox, DatePicker, Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import ButtonStyles from '../../../components/uiComponents/Button/ButtonStyle.module.css';
import { uploadNewFile } from '../../../services/dataIngestionApi';
import { showToast } from '../../../utils/helperFunctions/toastUtils';
import styles from './UploadExtractionFiles.module.css';
import { ModalComponents } from '../../../components/modalComponents';
import { DynamicFileUploadComponent } from '../../../components/reusableComponents/dynamicFileUploadComponent/DynamicFileUploadComponent';

export const UploadExtractionFiles = ({uploadFilesPopupOpen, setUploadFilesPopupOpen, blobFilesList }) => {

	const [selectedFiles, setSelectedFiles] = useState([]);
	const [loading, setLoading] = useState(false);
	const [reportDate, setReportDate] = useState();
	const [selectedOptions, setSelectedOptions] = useState([]);

	const checkboxOptions = ['PCOF', 'PFLT'];


	// const { getRootProps, getInputProps } = useDropzone({
	// 	accept: [
	// 		'text/csv',
	// 		'document/csv',
	// 		'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	// 	],
	// 	multiple: true,
	// 	onDrop: (acceptedFiles) => {
	// 		setSelectedFiles([...selectedFiles, ...acceptedFiles]);
	// 	}
	// });

	const handleCancel = () => {
		setSelectedFiles([]);
		setSelectedOptions([]);
		setUploadFilesPopupOpen(false);
		setReportDate();
	};


	const handleDateChange = (date, dateString) => {
		setReportDate(dateString);
	};

	const handleFileUpload = async() => {



		if (!reportDate || reportDate == "") {
			showToast('warning', "Select Report Date");
			return;
		}
		setLoading(true);
		try {
			const selectedFunds = selectedOptions;
			const uploadresponse = await uploadNewFile(selectedFiles, reportDate, selectedFunds);

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
							/>
							<div style={{ marginTop: '20px', marginBottom: '20px'}}>
								<Checkbox.Group
									options={checkboxOptions}
									value={selectedOptions}
									onChange={handleCheckboxChange}
								/>
							</div>
						</div>
						{/* <div className={styles.visible}>
							<div {...getRootProps({ className: 'dropzone' })}>
								<input {...getInputProps()} />
								<div>
									<span>
										<b>{selectedFiles?.length ? selectedFiles.map((file) => file.name).join(', ') : 'Drag and drop files here, or'}</b>
									</span>
									<span
										style={{
											color: '#3B7DDD',
											textDecoration: 'underline',
											cursor: 'pointer',
											marginLeft: '5px'
										}}
									>
										Browse
									</span>
								</div>
								<p className={styles.supportHeading}>Supported file format: CSV, XLSX</p>
							</div>
						</div> */}
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
