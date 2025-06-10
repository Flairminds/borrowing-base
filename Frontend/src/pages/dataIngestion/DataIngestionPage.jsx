import { Select, Modal } from 'antd';
import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router';
import { BackOption } from '../../components/BackOption/BackOption';
import { Calender } from '../../components/calender/Calender';
import { DynamicSwitchComponent } from '../../components/reusableComponents/dynamicSwichComponent/DynamicSwitchComponent';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from '../../components/uiComponents';
import { CustomButton } from '../../components/uiComponents/Button/CustomButton';
import { UploadExtractionFiles } from '../../modal/dataIngestionModals/uploadFilesModal/UploadExtractionFiles';
import { SrcFileValidationErrorModal } from '../../modal/srcFIleValidationErrorModal/srcFileValidationErrorModal';
import { exportBaseDataFile, getArchive, getBaseDataFilesList, getBaseFilePreviewData, getBlobFilesList, updateArchiveStatus } from '../../services/dataIngestionApi';
import { fundMap, fundOptionsArray, PAGE_ROUTES } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { STATUS_BG_COLOR, FUND_BG_COLOR } from '../../utils/styles';
import styles from './DataIngestionPage.module.css';
import { Icons } from '../../components/icons';
import { extractionFileStrings } from '../../utils/constants/constants';

export const DataIngestionPage = ({setBaseFilePreviewData, selectedIds}) => {

	const [dataIngestionFileListData, setDataIngestionFileListData] = useState();
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState();
	const [uploadFilesPopupOpen, setUploadFilesPopupOpen] = useState(false);
	const [previewBaseDataLoading, setPreviewBaseDataLoading] = useState(false);
	const [previewReportDate, setPreviewReportDate] = useState('');
	const [selectedFundType, setSelectedFundType] = useState(0);
	const [archiveToggle, setArchiveToggle] = useState(false);
	const [archiveFilesData, setArchiveFilesData] = useState(null);
	const [isbuttonDisable, setButtonDisable] = useState(false);
	const [dataLoading, setDataLoading] = useState(false);
	const [filteredData, setFilteredData] = useState([]);
	const [filterDate, setFilterDate] = useState(null);
	const [reportDates, setReportDates] = useState([]);
	const [extractionInProgress, setExtractionInProgress] = useState(false);
	const [filesSelected, setFilesSelected] = useState(0);
	const [unmappedSecurities, setUnmappedSecurities] = useState(0);
	const [showUnmappedSecuritiesModal, setShowUnmappedSecuritiesModal] = useState(false);

	const navigate = useNavigate();
	let extractionInterval;

	const blobFilesList = async(fundType) => {
		try {
			setDataLoading(true);
			const payload = fundMap[fundType] || null;
			const fileresponse = await getBlobFilesList(payload);
			const responseData = fileresponse.data.result;
			// const temp = responseData.data.map(d => {
			// 	return {
			// 		...d,
			// 		fund: d.fund.join(', ')
			// 	};
			// });
			// responseData.data = temp;
			const reportDatesArr = [];
			responseData?.data?.forEach(d => reportDatesArr.push(d.report_date));
			setReportDates(reportDatesArr);
			setDataIngestionFileListData(responseData.data);
			if (filterDate) {
				const temp = responseData.data.filter(t => t.report_date == filterDate);
				setFilteredData(temp);
			} else {
				setFilteredData(responseData.data);
			}

			const columnsToAdd = [{
				'key': 'file_select',
				'label': '',
				'render': (value, row) => {
					const isDisabled = row['extraction_status'] === 'In Progress' || row['extraction_status'] === 'Failed';
					return (
						<input
							checked={selectedIds.current.includes(row.file_id)}
							onClick={() => handleCheckboxClick(row.file_id)}
							type="checkbox"
							disabled={isDisabled}
						/>
					);
				}
			}];

			let updatedColumns = [...columnsToAdd, ...responseData.columns];
			updatedColumns = injectRender(updatedColumns);
			setDataIngestionFileListColumns(updatedColumns);
			setDataLoading(false);

		} catch (err) {
			console.error(err);
			showToast("error", err.response.data.message);
			setDataLoading(false);
		}
	};

	const injectRender = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'extraction_status') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{display: 'inline-block', padding: '3px 7px', borderRadius: '8px', ...(STATUS_BG_COLOR[row.extraction_status.toLowerCase()] || {backgroundColor: 'gray', color: 'white'})}}>
								{row.extraction_status}
							</span>
							{row.extraction_status === 'Failed' && row.validation_info &&
								<span
									style={{cursor: "pointer", paddingLeft: "3px"}}
									onClick={() => {
										const recordData = Object.entries(row);
										recordData.forEach((data) => {
											if (data[0] === "validation_info") {
												setShowErrorsModal(true);
												setValidationInfoData(data[1]);
											}
										});
									}}
								>
									Show more
								</span>
							}
						</div>
					)
				};
			}
			if (col.key === 'fund') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.fund.map((f, i) => {
								return (
									<span key={i} style={{display: 'inline-block', ...(FUND_BG_COLOR[f] || { backgroundColor: 'gray', color: 'white'}), padding: '3px 7px', margin: '0 2px', borderRadius: '8px'}}>
										{f}
									</span>
								);
							})}
						</div>
					)
				};
			}
			return col;
		});
	};

	const handleDropdownChange = (value) => {
		setSelectedFundType(value);
		blobFilesList(value);
	};

	useEffect(() => {
		blobFilesList(selectedFundType);
		selectedIds.current = [];
		// setSelectedIds([]);
	}, []);

	useEffect(() => {
		if (extractionInProgress) {
			const intervalRef = { current: null };
			intervalRef.current = setInterval(async() => {
				const payload = fundMap[selectedFundType] || null;
				const fileresponse = await getBlobFilesList(payload);
				const responseData = fileresponse.data.result;
				const inProgressCount = responseData.data.filter(r => !['completed', 'failed'].includes(r.extraction_status.toLowerCase())).length;
				console.log('File check interval running');
				if (inProgressCount == 0) {
					clearInterval(intervalRef.current);
					console.log('File check interval completed but running');
					showToast('success', 'All files extraction completed. Please refresh page.');
				}
			}, 5000);
			return () => {
				// Cleanup the interval on component unmount
				if (intervalRef.current) {
					clearInterval(intervalRef.current);
				}
			};
		}
	}, [extractionInProgress]);

	const handleCheckboxClick = (fileId) => {
		if (selectedIds?.current.indexOf(fileId) === -1) {
			// setSelectedIds([...selectedIds, fileId]);
			selectedIds.current = [...selectedIds.current, fileId];
			setFilesSelected(selectedIds.current.length);
			// setSelectedIds([...selectedIds, fileId]);
		} else {
			selectedIds.current = selectedIds?.current.filter(id => id !== fileId);
			setFilesSelected(selectedIds.current.length);
			// setSelectedIds(selectedIds.filter(id => id !== fileId));
		}
		console.info('sel ids', selectedIds);
	};

	const handleFileExtraction = async(e, ignoreUnmappedCheck = false) => {
		e.preventDefault();
		// setFileExtractionLoading(true);
		try {
			if (!selectedFundType) {
				alert('Please select a fund for data extraction.');
				return;
			}
			if (selectedIds.current.length == 0) {
				alert('Please select files.');
				return;
			}
			setExtractionInProgress(true);
			const selectedFund = fundMap[selectedFundType] || "";
			setBaseFilePreviewData([]);
			const extractionResponse = await exportBaseDataFile(selectedIds.current, selectedFund, ignoreUnmappedCheck);
			console.info(extractionResponse, 'rex');
			const extractionData = extractionResponse?.data.result;
			showToast("info", extractionResponse.data.message);
			// getExtractionStatus(9);

			extractionInterval = setInterval(() => getExtractionStatus(extractionData), 3000);
		} catch (err) {
			console.error(err);
			setExtractionInProgress(false);
			showToast("error", err.response.data.message);
			if (err.response.data.result && err.response.data.result.data.length > 0) {
				setUnmappedSecurities(err.response.data.result.data);
				setShowUnmappedSecuritiesModal(true);
			}
		}

		// setFileExtractionLoading(false);
	};

	const getExtractionStatus = async (extractData) => {
		try {
			const extractionStatusRes = await getBaseDataFilesList(extractData);
			const extractionStatus = extractionStatusRes.data.result.data[0].extraction_status;
			console.info(extractionStatus, 'status');
			if (extractionStatus !== "In progress") {
				console.info(extractionStatus, 'conditionn entered');
				clearInterval(extractionInterval);
			}
			if (extractionStatus === "Completed" ) {
				setExtractionInProgress(false);
				navigate(`/data-ingestion/base-data-preview/${extractData.id}`);
				return true;
			}
			setExtractionInProgress(false);
		} catch (err) {
			setExtractionInProgress(false);
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

			let updatedArchivedColumns = [...archivecolumnsToAdd, ...archiveData.columns];
			updatedArchivedColumns = injectRender(updatedArchivedColumns);
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

	const filterByDate = (value, dateString) => {
		try {
			if (dateString) {
				setFilterDate(dateString);
				let temp = [...dataIngestionFileListData];
				temp = temp.filter(t => t.report_date == dateString);
				setFilteredData(temp);
			} else {
				setFilterDate(null);
				setFilteredData(dataIngestionFileListData);
			}
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<>
			<div className={styles.ingestionPageContainer}>
				<div className={styles.ingestionPage}>
					<div className={styles.topBar}>
						<div style={{display: 'flex', alignItems: 'center'}}>
							<BackOption onClick={() => navigate(PAGE_ROUTES.BASE_DATA_LIST.url)} text={`<- Back`} />
							{!archiveToggle ? <><Select
								defaultValue={selectedFundType}
								style={{ width: 140, borderRadius: '8px', margin: '0rem 0.5rem' }}
								options={fundOptionsArray}
								onChange={handleDropdownChange}
							/>
							<div>
								<Calender availableClosingDates={reportDates} onDateChange={filterByDate} fileUpload={true} />
							</div>
							</> : <></>}
							{filesSelected > 0 &&
							<>
								{!isbuttonDisable && (
									<UIComponents.Button
										loading={extractionInProgress}
										loadingText='Extracting...'
										isFilled={true}
										onClick={(e) => handleFileExtraction(e)}
										text='Extract Base Data'
									// loading={fileExtractionLoading}
									/>
								)}
								<CustomButton isFilled={true} onClick={updateFilesArchiveStatus} text={archiveToggle ? 'Unarchive' : 'Add to Archives'} /></>}
						</div>
						<div className={styles.buttonsContainer}>
							<div className={styles.extractDataBtn}>
								<DynamicSwitchComponent switchOnText="Archives" switchOffText="Source Files" switchOnChange={toggleArchiveFiles} />
								<CustomButton isFilled={true} onClick={() => setUploadFilesPopupOpen(true)} text='+ Upload Files' />
							</div>
						</div>
					</div>
					<div><Icons.InfoIcon title={``} />{selectedFundType === 0 ? 'Select a fund type' : extractionFileStrings[selectedFundType]}</div>

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

					{dataLoading ? <UIComponents.Loader /> :
						<><div className={styles.tableContainer}>
							{
								archiveToggle ?
									<DynamicTableComponents data={archiveFilesData?.data} columns={archiveFilesData?.columns}	/>
									:
									<DynamicTableComponents data={filteredData} columns={dataIngestionFileListColumns} />
							}
						</div>
						</>}
				</div>
			</div>


			<UploadExtractionFiles
				uploadFilesPopupOpen={uploadFilesPopupOpen}
				setUploadFilesPopupOpen={setUploadFilesPopupOpen}
				blobFilesList={blobFilesList}
			/>

			<SrcFileValidationErrorModal
				isModalOpen={showErrorsModal}
				setIsModalOpen={setShowErrorsModal}
				validationInfoData={validationInfoData}
			/>
			<Modal title={""} open={showUnmappedSecuritiesModal} footer={null} onCancel={() => setShowUnmappedSecuritiesModal(false)} style={{marginTop: '-50px'}}>
				{unmappedSecurities.length > 0 &&
				<div>
					<p>{unmappedSecurities.length} unmapped securities</p>
					<ol>
						{unmappedSecurities.map((item, index) => {
							if (item) {
								return <li key={index}>{item.asset} [{item.type}]</li>;
							}
						})}
					</ol>
					<div>
						<UIComponents.Button
							onClick={() => setExtractionInProgress(false)}
							text='Cancel'
						// loading={fileExtractionLoading}
						/>
						<UIComponents.Button
							isFilled={true}
							btnDisabled={true}
							onClick={() => {}}
							text='Review Mapping'
						// loading={fileExtractionLoading}
						/>
						<UIComponents.Button
							loading={extractionInProgress}
							loadingText='Extracting...'
							isFilled={true}
							onClick={(e) => handleFileExtraction(e, true)}
							text='Proceed for Extraction'
						// loading={fileExtractionLoading}
						/>
					</div>
				</div>}
			</Modal>
		</>
	);
};