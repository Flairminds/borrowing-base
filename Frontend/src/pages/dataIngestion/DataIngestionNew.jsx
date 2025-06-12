import { SearchOutlined, CloseOutlined } from '@ant-design/icons';
import { Input, Modal, Select } from 'antd';
import React, { useState, useMemo, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router';
import { Calender } from '../../components/calender/Calender';
import { DataMapping } from '../../components/dataIngestionSteps/DataMapping';
import { ExtractBaseData } from '../../components/dataIngestionSteps/ExtractBaseData';
import FundReport from '../../components/dataIngestionSteps/FundReport';
import ProgressBar from '../../components/dataIngestionSteps/ProgressBar/ProgressBar';
import { SelectFiles } from '../../components/dataIngestionSteps/SelectFiles';
import SelectFundDate from '../../components/dataIngestionSteps/SelectFundDate/SelectFundDate';
import { UploadFiles } from '../../components/dataIngestionSteps/UploadFiles';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import { UIComponents } from '../../components/uiComponents';
import { LoaderSmall } from '../../components/uiComponents/loader/loader';
import { exportBaseDataFile, getBaseDataFilesList, getBlobFilesList } from '../../services/dataIngestionApi';
import { fundMap, fundOptionsArray } from '../../utils/constants/constants';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import { FUND_BG_COLOR, STATUS_BG_COLOR } from '../../utils/styles';
import styles from './DataIngestionPage.module.css';


const BaseDataTab = () => {
	// Extract New Base Data
	const [isExtractionMode, setIsExtractionMode] = useState(false);
	const [currentStep, setCurrentStep] = useState(0);
	const [selectedFund, setSelectedFund] = useState(fundOptionsArray[0].label);
	const [selectedDate, setSelectedDate] = useState(null);

	const [selectedFiles, setSelectedFiles] = useState([]);
	const [uploadedFiles, setUploadedFiles] = useState([]);
	const selectedIds = useRef([]);

	const stepContent = [
		<SelectFundDate
			key="step1"
			selectedFund={selectedFund}
			setSelectedFund={setSelectedFund}
			selectedDate={selectedDate}
			setSelectedDate={setSelectedDate}
		/>,
		<UploadFiles
			key="step2"
			selectedFund={selectedFund}
			selectedDate={selectedDate}
			uploadedFiles={uploadedFiles}
			setUploadedFiles={setUploadedFiles}
		/>,
		<SelectFiles
			key="step3"
			uploadedFiles={uploadedFiles}
			selectedFiles={selectedFiles}
			setSelectedFiles={setSelectedFiles}
			selectedIds={selectedIds}
		/>,
		<DataMapping
			key="step4"
			selectedFund={selectedFund}
			selectedDate={selectedDate}
			selectedFiles={selectedFiles}
		/>,
		<ExtractBaseData
			key="step5"
			selectedIds={selectedIds}
			uploadedFiles={uploadedFiles}
		/>
	];

	const [extractionInProgress, setExtractionInProgress] = useState(false);
	const [unmappedSecurities, setUnmappedSecurities] = useState([]);
	const [showUnmappedSecuritiesModal, setShowUnmappedSecuritiesModal] = useState(false);

	const navigate = useNavigate();
	let extractionInterval;

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

	const handleStartExtraction = async (ignoreUnmappedCheck = false) => {
		try {
			setExtractionInProgress(true);
			// setBaseFilePreviewData([]);
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

	if (isExtractionMode) {
		return (
			<>
				<div style={{ background: '#fff', borderRadius: 8, padding: 24 }}>
					<div style={{ marginBottom: 24 }}>
						<div style={{ fontSize: 24, fontWeight: 600 }}>Extract new Base Data</div>
					</div>
					<ProgressBar currentStep={currentStep} />
					{currentStep !== 0 &&
						<FundReport selectedDate={selectedDate} selectedFund={selectedFund} />
					}
					<div style={{ minHeight: 240 }}>{stepContent[currentStep]}</div>
					<div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 32 }}>
						<UIComponents.Button
							text="Back"
							disabled={currentStep === 0}
							btnDisabled={currentStep === 0 ? true : false}
							onClick={() => setCurrentStep(s => s - 1)}
							customStyle={{ minWidth: 100 }}
						/>
						<UIComponents.Button
							text={currentStep === stepContent.length - 1 ? 'Start Extraction' : 'Next'}
							isFilled={true}
							onClick={() => {
								if (currentStep < stepContent.length - 1) {
									setCurrentStep(s => s + 1);
								} else {
									handleStartExtraction();
								}
							}}
							customStyle={{ minWidth: 100 }}
							btnDisabled={(selectedDate && selectedFund !== "-- Select Fund --") ? false : true }
							loading={extractionInProgress}
						/>
					</div>
				</div>
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
								onClick={(e) => handleStartExtraction(e, true)}
								text='Extract Base Data'
							// loading={fileExtractionLoading}
							/>
						</div>
					</div>}
				</Modal>
			</>
		);
	}

	const [reportDates, setReportDates] = useState(null);
	const [fund, setFund] = useState(fundOptionsArray[0].label);
	const [filteredData, setFilteredData] = useState([]);
	const [dataLoading, setDataLoading] = useState(false);
	const [baseDataFilesList, setBaseDataFilesList] = useState([]);

	useEffect(() => {
		getFilesList();
	}, []);

	const injectRenderForSourceFiles = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'source_files') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.source_file_details?.map((file, index) => (
								<div
									key={file.file_id}
									// onClick={() => handleSourceFileClick(file)}
									style={{
										color: '#007BFF',
										cursor: 'pointer',
										textDecoration: 'underline',
										marginBottom: '2px'
									}}
								>
									{index + 1}. {file.file_name + file.extension}
								</div>
							))}
						</div>
					)
				};
			}
			if (col.key === 'extraction_status') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{display: 'inline-block', padding: '3px 7px', borderRadius: '8px', ...(STATUS_BG_COLOR[row.extraction_status.toLowerCase()] || { backgroundColor: 'gray', color: 'white'})}}>
								{row.extraction_status.split(" ")
									.map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
									.join(" ")}
							</span>
						</div>
					)
				};
			}
			if (col.key === 'fund') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{display: 'inline-block', padding: '3px 7px', borderRadius: '8px', ...(FUND_BG_COLOR[row.fund] || { backgroundColor: 'gray', color: 'white'})}}>
								{row.fund}
							</span>
						</div>
					)
				};
			}
			return col;
		});
	};

	const getFilesList = async (fundType) => {
		const Fund = fundMap[fundType];
		try {
			setDataLoading(true);
			const data = {
				"company_id": 1,
				"fund_type": Fund
			};
			const filesRes = await getBaseDataFilesList(data);
			const updatedColumns = injectRenderForSourceFiles(filesRes.data.result.columns);
			setBaseDataFilesList({ ...filesRes.data.result, columns: updatedColumns });
			const reportDatesArr = [];
			filesRes.data.result?.data?.forEach(d => reportDatesArr.push(d.report_date));
			setReportDates(reportDatesArr);
			setDataLoading(false);
			setFilteredData(filesRes.data.result.data);
		} catch (err) {
			showToast('error', err?.response?.data.message);
			setDataLoading(false);
		}
	};

	const handleDateChange = (date, dateString) => {
		if (date) {
			const selectedReportDateFiles = baseDataFilesList?.data.filter(item => {
				if (fund !== "-- Select Fund --") {
					return item.report_date === dateString && item.fund === fundOptionsArray[fund].label;
				} else {
					return item.report_date === dateString;
				}
			});
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(baseDataFilesList?.data);
			setFund(0);
		}
	};

	const handleDropdownChange = (fund) => {
		if ( fundOptionsArray[fund].label !== "-- Select Fund --") {
			const choosedFund = fundOptionsArray[fund].label;
			const selectedReportDateFiles = baseDataFilesList?.data.filter(item => item.fund === choosedFund);
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(baseDataFilesList?.data);
		}
		setFund(fund);
	};

	return (
		<>
			<div style={{ background: '#fff', borderRadius: 8, padding: 24 }}>
				<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
					<h1 style={{ fontSize: 24, fontWeight: 600 }}>Extracted Base Data</h1>
					<div style={{ display: 'flex', alignItems: "center", gap: 2 }}>
						<div style={{ padding: '0 5px 0 0' }}>
							<div style={{display: "flex", alignItems: "center", padding: "0 5px 0 7px"}}>
								<Calender
									fileUpload={true}
									availableClosingDates={reportDates}
									onDateChange={handleDateChange}
								/>
							</div>
						</div>
						<div style={{ padding: '0 5px 0 0' }}>
							<Select
								defaultValue={fundOptionsArray[0].label}
								style={{ width: 150, borderRadius: '8px', margin: "0.5rem 0rem" }}
								onChange={handleDropdownChange}
								value={fund}
								options={fundOptionsArray}
							/>
						</div>
						<UIComponents.Button
							text="+ Extract New Base Data"
							isFilled={true}
							onClick={() => setIsExtractionMode(true)}
						/>
					</div>
				</div>
				{dataLoading ? <LoaderSmall /> :
					<div className={styles.baseDataTableContainer}>
						<DynamicTableComponents data={filteredData} columns={baseDataFilesList?.columns} />
					</div>
				}
			</div>
		</>
	);
};

const SourceFilesTab = () => {
	const [selectedIds, setSelectedIds] = useState([]);
	const [uploadedSourceFiles, setUploadedSourceFiles] = useState({ data: [], columns: [] });
	const [dataLoading, setDataLoading] = useState(false);

	useEffect(() => {
		blobFilesList();
	}, []);

	const blobFilesList = async () => {
		const fundType = null;
		setDataLoading(true);
		try {
			const blobResponse = await getBlobFilesList(fundType);
			setUploadedSourceFiles(blobResponse.data.result || { data: [], columns: [] });
		} catch (err) {
			console.error(err);
			showToast("error", err.response?.data?.message || "Error loading files");
		} finally {
			setDataLoading(false);
		}
	};

	const toggleSelection = (fileId) => {
		setSelectedIds(prev =>
			prev.includes(fileId)
				? prev.filter(id => id !== fileId)
				: [...prev, fileId]
		);
	};

	return (
		<div style={{ padding: '24px' }}>
			<div style={{ background: '#fff', borderRadius: 8}}>
				<div style={{ fontSize: 22, fontWeight: 600, marginBottom: 24 }}>Uploaded Source Files</div>
				{dataLoading ? <LoaderSmall /> : (
					<SourceFileTable
						uploadedFiles={uploadedSourceFiles}
						selectedIds={selectedIds}
						toggleSelection={toggleSelection}
					/>
				)}
			</div>
		</div>
	);
};

const SourceFileTable = ({ uploadedFiles, selectedIds, toggleSelection }) => {
	const [showErrorsModal, setShowErrorsModal] = useState(false);
	const [validationInfoData, setValidationInfoData] = useState([]);
	const [dataIngestionFileListColumns, setDataIngestionFileListColumns] = useState([]);

	const [fund, setFund] = useState(fundOptionsArray[0].label);
	const [filteredData, setFilteredData] = useState([]);
	const [searchText, setSearchText] = useState('');
	const [reportDates, setReportDates] = useState(null);

	// Initialize table columns
	useEffect(() => {
		const columnsToAdd = [{
			key: 'file_select',
			label: '',
			render: (value, row) => {
				const isDisabled = ['In Progress', 'Failed'].includes(row.extraction_status);
				return (
					<div style={{ display: 'flex', alignItems: 'center' }}>
						<input
							checked={selectedIds.includes(row.file_id)}
							onChange={() => toggleSelection(row.file_id)}
							type="checkbox"
							disabled={isDisabled}
							style={{ transform: 'scale(1.3)' }}
						/>
					</div>
				);
			}
		}];

		const updatedColumns = injectRender([...columnsToAdd, ...uploadedFiles.columns]);
		setDataIngestionFileListColumns(updatedColumns);
	}, [uploadedFiles.columns, selectedIds, toggleSelection]);

	// Filter data based on search
	useEffect(() => {
		const filtered = uploadedFiles?.data?.filter(item =>
			item?.file_name?.toLowerCase().includes(searchText.toLowerCase())
		);
		setFilteredData(filtered);
	}, [searchText, uploadedFiles]);

	useEffect(() => {
		const reportDateList = uploadedFiles?.data?.map(item => {
			if (item?.report_date) {
				return item.report_date;
			}
		});
		setReportDates(reportDateList);
	}, [uploadedFiles]);

	const injectRender = (columns) => {
		return columns?.map((col) => {
			if (col.key === 'extraction_status') {
				return {
					...col,
					render: (value, row) => (
						<div>
							<span style={{
								display: 'inline-block',
								padding: '3px 7px',
								borderRadius: '8px',
								...(STATUS_BG_COLOR[row.extraction_status?.toLowerCase()] || {})
							}}>
								{row.extraction_status}
							</span>
							{row.extraction_status === 'Failed' && row.validation_info && (
								<span
									style={{ cursor: "pointer", paddingLeft: "3px" }}
									onClick={() => {
										setShowErrorsModal(true);
										setValidationInfoData(row.validation_info);
									}}
								>
									Show more
								</span>
							)}
						</div>
					)
				};
			}
			if (col.key === 'fund') {
				return {
					...col,
					render: (value, row) => (
						<div>
							{row.fund?.map((f, i) => (
								<span
									key={i}
									style={{
										display: 'inline-block',
										...(FUND_BG_COLOR[f] || {}),
										padding: '3px 7px',
										margin: '0 2px',
										borderRadius: '8px'
									}}
								>
									{f}
								</span>
							))}
						</div>
					)
				};
			}
			return col;
		});
	};

	const handleDropdownChange = (fund) => {
		if ( fundOptionsArray[fund].label !== "-- Select Fund --") {
			const choosedFund = fundOptionsArray[fund].label;
			const selectedReportDateFiles = uploadedFiles?.data.filter(item => item.fund.includes(choosedFund));
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(uploadedFiles?.data);
		}
		setFund(fund);
	};

	const handleDateChange = (date, dateString) => {
		if (date) {
			const selectedReportDateFiles = uploadedFiles?.data.filter(item => {
				if (fund !== "-- Select Fund --") {
					return item.report_date === dateString;
				} else {
					return item.report_date === dateString;
				}
			});
			setFilteredData(selectedReportDateFiles);
		} else {
			setFilteredData(uploadedFiles?.data);
		}
		setFund(0);
	};

	const handleSearch = (value) => {
		setSearchText(value);
	};

	const handleClearSearch = () => {
		setSearchText('');
	};

	return (
		<>
			<div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 18 }}>
				<span style={{ fontWeight: 500 }}>Filter by:</span>
				<Select
					defaultValue={fundOptionsArray[0].label}
					style={{ width: 150, borderRadius: '8px', margin: "0.5rem 0rem" }}
					onChange={handleDropdownChange}
					value={fund}
					options={fundOptionsArray}
				/>
				<Calender
					fileUpload={true}
					availableClosingDates={reportDates}
					onDateChange={handleDateChange}
				/>
				<Input
					placeholder="Search by file name"
					value={searchText}
					onChange={(e) => handleSearch(e.target.value)}
					style={{ width: 200 }}
					suffix={
						searchText ?
							<CloseOutlined style={{ cursor: 'pointer' }} onClick={handleClearSearch} /> :
							<SearchOutlined />
					}
				/>
				<div style={{ flex: 1 }} />
				<UIComponents.Button text="View Archived" customStyle={{ background: '#2966d8', color: '#fff' }} />
				<UIComponents.Button
					text="Archive Selected"
					customStyle={{ background: '#ffe58f', color: '#ad6800' }}
					// disabled={selectedRows.length === 0}
				/>
				<UIComponents.Button
					text="Delete Selected"
					customStyle={{ background: '#ff7875', color: '#fff' }}
					// disabled={selectedRows.length === 0}
				/>
			</div>
			<DynamicTableComponents
				data={filteredData}
				columns={dataIngestionFileListColumns}
			/>
		</>
	);
};

const tabItems = [
	{ key: 'baseData', label: 'Base Data', children: <BaseDataTab /> },
	{ key: 'sourceFiles', label: 'Source Files', children: <SourceFilesTab /> }
];

const DataIngestionNew = () => {
	const [activeKey, setActiveKey] = useState('baseData');
	return (
		<div className={styles.dataIngestionPageContainer}>
			<div className={styles.tabs}>
				{tabItems.map(tab => (
					<div
						key={tab.key}
						className={`${styles.tab} ${activeKey === tab.key ? styles.activeTab : ''}`}
						onClick={() => setActiveKey(tab.key)}
					>
						{tab.label}
					</div>
				))}
			</div>
			<div className={styles.tabContent}>
				{tabItems.find(tab => tab.key === activeKey)?.children}
			</div>
		</div>
	);
};

export default DataIngestionNew;