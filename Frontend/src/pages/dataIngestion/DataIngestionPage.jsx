import { DatePicker, Select } from 'antd';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { BackOption } from '../../components/BackOption/BackOption';
import { CustomButton } from '../../components/custombutton/CustomButton';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UploadExtractionFiles } from '../../modal/dataIngestionModals/uploadFilesModal/UploadExtractionFiles';
import { exportBaseDataFile, getArchive, getBaseDataFilesList, getBaseFilePreviewData, getBlobFilesList, updateArchiveStatus } from '../../services/dataIngestionApi';
import { fundOptionsArray } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import styles from './DataIngestionPage.module.css';
import { DynamicSwitchComponent } from '../../components/reusableComponents/dynamicSwichComponent/DynamicSwitchComponent';

export const DataIngestionPage = ({setBaseFilePreviewData, selectedIds}) => {

	const [dataIngestionFileListData, setDataIngestionFileListData] = useState();
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState();
	const [uploadFilesPopupOpen, setUploadFilesPopupOpen] = useState(false);
	const [previewBaseDataLoading, setPreviewBaseDataLoading] = useState(false);
	const [previewReportDate, setPreviewReportDate] = useState('');
	const [selectedFundType, setSelectedFundType] = useState(2);
	const [archiveToggle, setArchiveToggle] = useState(false);
	const [archiveFilesData, setArchiveFilesData] = useState(null);
	const [isbuttonDisable, setButtonDisable] = useState(false);

	const navigate = useNavigate();
	let extractionInterval;

	const blobFilesList = async(fundType) => {
		try {
			const payload = fundType === 1 ? 'PCOF' : 'PFLT';
			const fileresponse = await getBlobFilesList(payload);
			const responseData = fileresponse.data.result;

			setDataIngestionFileListData(responseData.data);

			const columnsToAdd = [{
				'key': 'file_select',
				'label': '',
				'render': (value, row) => <input checked={selectedIds.current.includes(row.file_id)} onClick={() => handleCheckboxClick(row.file_id)} type="checkbox" />
			}];

			const updatedcolumns = [...columnsToAdd, ...responseData.columns];
			setDataIngestionFileListColumns(updatedcolumns);

		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		}
	};

	const handleDropdownChange = (value) => {
		setSelectedFundType(value);
		if (value !== 0) {
			blobFilesList(value);
		}
	};

	useEffect(() => {
		blobFilesList(selectedFundType);
		selectedIds.current = [];
		// setSelectedIds([]);
	}, []);

	const handleCheckboxClick = (fileId) => {
		if (selectedIds?.current.indexOf(fileId) === -1) {
			// setSelectedIds([...selectedIds, fileId]);
			selectedIds.current = [...selectedIds.current, fileId];
			// setSelectedIds([...selectedIds, fileId]);
		} else {
			selectedIds.current = selectedIds?.current.filter(id => id !== fileId);
			// setSelectedIds(selectedIds.filter(id => id !== fileId));
		}
		console.info('sel ids', selectedIds);
	};

	const handleFileExtraction = async() => {
		// setFileExtractionLoading(true);
		try {
			const extractionResponse = await exportBaseDataFile(selectedIds.current);
			console.info(extractionResponse, 'rex');
			const extractionData = extractionResponse?.data.result;
			showToast("info", extractionResponse.data.message);
			// getExtractionStatus(9);

			extractionInterval = setInterval(() => getExtractionStatus(extractionData), 5000);
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		}

		// setFileExtractionLoading(false);
	};

	const getExtractionStatus = async (extractData) => {
		try {
			const extractionStatusRes = await getBaseDataFilesList(extractData);
			const extractionStatus = extractionStatusRes.data.result.data[0].extraction_status;
			console.info(extractionStatus, 'status');
			if (extractionStatus !== "In Progress") {
				console.info(extractionStatus, 'conditionn entered');
				clearInterval(extractionInterval);
			}
			if (extractionStatus === "completed" ) {
				return true;
			}
		} catch (err) {
			showToast('failure', err?.response?.data.message);
		}

		return false;

	};

	const handleDateChange = (date, dateString) => {
		setPreviewReportDate(dateString);
	};

	const handleBaseDataPreview = async() => {
		if (!previewReportDate || previewReportDate == "") {
			showToast('warning', "Select report Date");
			return;
		}
		setPreviewBaseDataLoading(true);

		try {
			const previewDataResponse = await getBaseFilePreviewData(previewReportDate, 1);
			console.info(previewDataResponse, 'base preview ');
			setBaseFilePreviewData(previewDataResponse.data.result);
			navigate('/base-data-preview');
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		}
		setPreviewBaseDataLoading(false);
	};

	const getArchiveFiles = async() => {
		try {
			const res = await getArchive();
			const archiveData = res.data.result.data;
			const archivecolumnsToAdd = [{
				'key': 'file_select',
				'label': '',
				'render': (value, row) => <input checked={selectedIds.current.includes(row.file_id)} onClick={() => handleCheckboxClick(row.file_id)} type="checkbox" />
			}];

			const updatedArchivedColumns = [...archivecolumnsToAdd, ...archiveData.columns];
			const updatedArchivedData = {
				...archiveData,
				columns: updatedArchivedColumns
			};
			setArchiveFilesData(updatedArchivedData);
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		}
	};

	const toggleArchiveFiles = (value) => {
		setButtonDisable(value);
		if (value) {
			getArchiveFiles();
		}
		selectedIds.current = [];
		setArchiveToggle(value);
	};

	const updateFilesArchiveStatus = async() => {
		console.info(selectedIds, 'ids');
		try {
			const res = await updateArchiveStatus(selectedIds.current, !archiveToggle);
			// setSelectedIds([]);
			selectedIds.current = [];
			// if (!archiveToggle) {
			await blobFilesList(selectedFundType);
			await getArchiveFiles();
			// } else {
			// }
		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
		}
	};

	return (
		<>
			<div className={styles.ingestionPageContainer}>
				<div className={styles.ingestionPage}>
					<div className={styles.buttonsContainer}>
						<div className={styles.backOptionContainer}>
							<div style={{ display: 'flex', flexDirection: 'row', alignItems: 'baseline' }}>
								<BackOption onClick={() => navigate('/base-data-list')}
									text={`<- Base Data`} />

								<div style={{ padding: '0 5px 0 0' }}></div>
								<Select
									defaultValue={selectedFundType}
									style={{ width: 140, borderRadius: '8px', margin: '1rem 1rem' }}
									options={fundOptionsArray}
									onChange={handleDropdownChange}
								/>
							</div>
						</div>
						<div className={styles.uploadFileBtnContainer}>
							<DynamicSwitchComponent switchOnText="Archives" switchOffText="Source Files" switchOnChange={toggleArchiveFiles} />
							<CustomButton isFilled={true} onClick={updateFilesArchiveStatus} text={archiveToggle ? 'Unarchive' : 'Add to Archives'} />
							<CustomButton isFilled={true} onClick={() => setUploadFilesPopupOpen(true)} text='+ Upload Files' />
						</div>
					</div>

					{/* <div className={styles.buttonsContainer}>
							<div className={styles.uploadFileBtnContainer}>
							<DatePicker
								placeholder='Report Date'
								onChange={handleDateChange}
								allowClear={true}
							/>
							<CustomButton
								isFilled={true}
								onClick={handleBaseDataPreview}
								text='Preview Base Data'
								loading={previewBaseDataLoading}
								loadingText="Fetching Data"
							/>
							</div>
						</div> */}

					<div className={styles.tableContainer}>
						{
							archiveToggle ?
								<DynamicTableComponents data={archiveFilesData?.data} columns={archiveFilesData?.columns}	/>
								:
								<DynamicTableComponents data={dataIngestionFileListData} columns={dataIngestionFileListColumns} />
						}
					</div>

					<div className={styles.extractDataBtn}>
					{!isbuttonDisable && (
						<CustomButton
							isFilled={true}
							onClick={handleFileExtraction}
							text='Extract Base Data'
							// loading={fileExtractionLoading}
						/>
					)}
					</div>
				</div>
			</div>


			<UploadExtractionFiles
				uploadFilesPopupOpen={uploadFilesPopupOpen}
				setUploadFilesPopupOpen={setUploadFilesPopupOpen}
				blobFilesList={blobFilesList}
			/>
		</>
	);
};