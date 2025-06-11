import React, { useState, useMemo, useEffect, useRef } from 'react';
import { DatePicker, Modal, Select } from 'antd';
import { CalendarOutlined, UploadOutlined, FolderOpenOutlined, ProfileOutlined, SettingOutlined } from '@ant-design/icons';
import styles from './DataIngestionPage.module.css';
import { UIComponents } from '../../components/uiComponents';
import { DynamicTableComponents } from '../../components/reusableComponents/dynamicTableComponent/DynamicTableComponents';
import SelectFundDate from '../../components/dataIngestionSteps/SelectFundDate/SelectFundDate';
import { UploadFiles } from '../../components/dataIngestionSteps/UploadFiles';
import { SelectFiles } from '../../components/dataIngestionSteps/SelectFiles';
import { DataMapping } from '../../components/dataIngestionSteps/DataMapping';
import { ExtractBaseData } from '../../components/dataIngestionSteps/ExtractBaseData';
import { fundMap, fundOptionsArray } from '../../utils/constants/constants';
import ProgressBar from '../../components/dataIngestionSteps/ProgressBar/ProgressBar';
import { Calender } from '../../components/calender/Calender';
import { Icons } from 'react-toastify';
import CalendarIcon from '../../assets/NavbarIcons/Calendar.svg';
import { exportBaseDataFile, getBaseDataFilesList } from '../../services/dataIngestionApi';
import { showToast } from '../../utils/helperFunctions/toastUtils';
import FundReport from '../../components/dataIngestionSteps/FundReport';
import { useNavigate } from 'react-router';

const mockBaseData = [
  {
    key: '231',
    reportDate: { value: '2025-06-03', meta_info: { display_value: '2025-06-03' } },
    fund: { value: 'PSSL', meta_info: { display_value: 'PSSL' } },
    extractionStatus: { value: 'Failed', meta_info: { display_value: 'Failed' } },
    extractionDate: { value: '2025-06-05', meta_info: { display_value: '2025-06-05' } },
    sourceFiles: { value: ['New Master Comps PSSL v4.xlsx', 'PSSLF221 CashFile 20250228 4.xlsm'], meta_info: { display_value: '2 files' } },
    action: { value: 'Errors', meta_info: { display_value: 'Errors' } }
  },
  {
    key: '230',
    reportDate: { value: '2025-06-03', meta_info: { display_value: '2025-06-03' } },
    fund: { value: 'PSSL', meta_info: { display_value: 'PSSL' } },
    extractionStatus: { value: 'Failed', meta_info: { display_value: 'Failed' } },
    extractionDate: { value: '2025-06-05', meta_info: { display_value: '2025-06-05' } },
    sourceFiles: { value: ['New Master Comps PSSL v4 dsk', 'PSSLF221 CashFile 20250228 4.xlsm'], meta_info: { display_value: '2 files' } },
    action: { value: 'Errors', meta_info: { display_value: 'Errors' } }
  },
  {
    key: '229',
    reportDate: { value: '2025-06-05', meta_info: { display_value: '2025-06-05' } },
    fund: { value: 'PCOF', meta_info: { display_value: 'PCOF' } },
    extractionStatus: { value: 'Completed', meta_info: { display_value: 'Completed' } },
    extractionDate: { value: '2025-06-05', meta_info: { display_value: '2025-06-05' } },
    sourceFiles: { value: ['Market-and-Book-Value-Position 20250520 100604-24 dsx', 'Super Master Comps March-1545263523.xlsx'], meta_info: { display_value: '2 files' } },
    action: { value: 'Preview Base Data', meta_info: { display_value: 'Preview Base Data' } }
  },
  {
    key: '228',
    reportDate: { value: '2025-04-30', meta_info: { display_value: '2025-04-30' } },
    fund: { value: 'PCOF', meta_info: { display_value: 'PCOF' } },
    extractionStatus: { value: 'Completed', meta_info: { display_value: 'Completed' } },
    extractionDate: { value: '2025-05-30', meta_info: { display_value: '2025-05-30' } },
    sourceFiles: { value: ['Market-and-Book-Value-Position 20250520 100604-24 xlsx', 'Super Master Comps yMarch-24.xlsx'], meta_info: { display_value: '2 files' } },
    action: { value: 'Preview Base Data', meta_info: { display_value: 'Preview Base Data' } }
  },
  {
    key: '227',
    reportDate: { value: '2025-04-30', meta_info: { display_value: '2025-04-30' } },
    fund: { value: 'PCOF', meta_info: { display_value: 'PCOF' } },
    extractionStatus: { value: 'Completed', meta_info: { display_value: 'Completed' } },
    extractionDate: { value: '2025-05-28', meta_info: { display_value: '2025-05-28' } },
    sourceFiles: { value: ['Market-and-Book-Value-Position 20250520 100604-24 8x', 'Super Master Comps viMarch-24.xlsx'], meta_info: { display_value: '2 files' } },
    action: { value: 'Preview Base Data', meta_info: { display_value: 'Preview Base Data' } }
  }
];

const mockSourceFiles = [
  { 
    key: '1', 
    name: { value: 'report_Q1_2025.xlsx', meta_info: { display_value: 'report_Q1_2025.xlsx' } },
    fund: { value: 'PSSL', meta_info: { display_value: 'PSSL' } },
    reportDate: { value: '2025-01-15', meta_info: { display_value: '2025-01-15' } },
    uploadedAt: { value: '10:30 AM', meta_info: { display_value: '10:30 AM' } },
    uploadedBy: { value: 'John Doe', meta_info: { display_value: 'John Doe' } }
  },
  { 
    key: '2', 
    name: { value: 'data_feb_2025.csv', meta_info: { display_value: 'data_feb_2025.csv' } },
    fund: { value: 'PCOF', meta_info: { display_value: 'PCOF' } },
    reportDate: { value: '2025-02-20', meta_info: { display_value: '2025-02-20' } },
    uploadedAt: { value: '02:45 PM', meta_info: { display_value: '02:45 PM' } },
    uploadedBy: { value: 'Jane Smith', meta_info: { display_value: 'Jane Smith' } }
  },
  { 
    key: '3', 
    name: { value: 'analysis_march_2025.xlsx', meta_info: { display_value: 'analysis_march_2025.xlsx' } },
    fund: { value: 'PSSL', meta_info: { display_value: 'PSSL' } },
    reportDate: { value: '2025-03-10', meta_info: { display_value: '2025-03-10' } },
    uploadedAt: { value: '09:10 AM', meta_info: { display_value: '09:10 AM' } },
    uploadedBy: { value: 'Alice Brown', meta_info: { display_value: 'Alice Brown' } }
  },
  { 
    key: '4', 
    name: { value: 'customer_data_2025.csv', meta_info: { display_value: 'customer_data_2025.csv' } },
    fund: { value: 'PCOF', meta_info: { display_value: 'PCOF' } },
    reportDate: { value: '2025-05-05', meta_info: { display_value: '2025-05-05' } },
    uploadedAt: { value: '01:15 PM', meta_info: { display_value: '01:15 PM' } },
    uploadedBy: { value: 'Alice Brown', meta_info: { display_value: 'Alice Brown' } }
  },
];

const columns = [
  { key: 'key', label: '#', isEditable: false },
  { key: 'reportDate', label: 'REPORT DATE', isEditable: false },
  { key: 'fund', label: 'FUND', isEditable: false },
  { key: 'extractionStatus', label: 'EXTRACTION STATUS', isEditable: false },
  { key: 'extractionDate', label: 'EXTRACTION DATE', isEditable: false },
  { key: 'sourceFiles', label: 'SOURCE FILES', isEditable: false },
  { key: 'action', label: '', isEditable: false }
];

const stepTitles = [
	'Select Fund & Date',
	'Upload source files',
	'Select files for extraction',
	'Data mapping',
	'Extract Base data',
];

const BaseDataTab = () => {
	const [isExtractionMode, setIsExtractionMode] = useState(false);
	const [currentStep, setCurrentStep] = useState(0);
	const [selectedFund, setSelectedFund] = useState(fundOptionsArray[0].label);
	const [selectedDate, setSelectedDate] = useState(null);
	const [filterFund, setFilterFund] = useState('');
	const [filterDate, setFilterDate] = useState(null);
	const [selectedFiles, setSelectedFiles] = useState([]);
	const [uploadedFiles, setUploadedFiles] = useState([]);
	const selectedIds = useRef([]);

	const filteredBaseData = useMemo(() => {
		return mockBaseData.filter(item => {
			const matchesFund = !filterFund || item.fund.value === filterFund;
			const matchesDate = !filterDate || item.reportDate.value === filterDate;
			return matchesFund && matchesDate;
		});
	}, [filterFund, filterDate]);

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

	const [selectedReportDate, setSelectedReportDate] = useState(null);
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
									onClick={() => handleSourceFileClick(file)}
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
			if (filterDate) {
				const temp = filesRes.data.result.data.filter(t => t.report_date == filterDate);
				setFilteredData(temp);
			} else {
				setFilteredData(filesRes.data.result.data);
			}
		} catch (err) {
			showToast('error', err?.response?.data.message);
			setDataLoading(false);
		}
	};

	const handleDateChange = (date, dateString) => {
		setSelectedReportDate(date); // `date` is a Day.js or Moment object depending on your setup
		console.log('Selected Date:', dateString); // Useful for debugging
	};

	const handleDropdownChange = (fund) => {
		const choosedFund = fundOptionsArray[fund].label;
		console.log("ch", choosedFund);
		setFund(fund);
	};

	const columnsToAdd = [{
		'key': 'file_preview',
		'label': '',
		'render': (value, row) => <div onClick={() => {
			// handleBaseDataPreview(row),
			console.log("Hii")
		}}
			style={{color: row.extraction_status.toLowerCase() === "completed" ? 'green' : 'red', cursor: 'pointer'}} title={row.extraction_status.toLowerCase() === "completed" ? 'Click to preview base data' : 'Click to view errors' } >
			{row.extraction_status.toLowerCase() === "completed" ? 'Preview Base Data' : (row.extraction_status.toLowerCase() === "failed" ? 'Errors' : '')}
		</div>
	}];

	return (
		<>
			<div style={{ background: '#fff', borderRadius: 8, padding: 24 }}>
				<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
					<h1 style={{ fontSize: 24, fontWeight: 600 }}>Extracted Base Data</h1>
					<div style={{ display: 'flex', alignItems: "center", gap: 12 }}>
						<div style={{ padding: '0 5px 0 0' }}>
							<div style={{display: "flex", alignItems: "center", padding: "0 5px 0 7px"}}>
								<DatePicker
									id="reportDatePicker"
									style={{ width: 130 }}
									suffixIcon={<img src={CalendarIcon} alt="calendar icon" />}
									placeholder="Report Date"
									allowClear={true}
									onChange={handleDateChange}
									value={selectedReportDate}
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
				{/* <div className={styles.baseDataTableContainer}>
					<DynamicTableComponents data={filteredData} columns={baseDataFilesList?.columns} />
				</div> */}
			</div>
		</>
	);
};

const SourceFilesTab = () => {
  const [selectedRows, setSelectedRows] = useState([]);
  const [fundFilter, setFundFilter] = useState('');
  const [dateFilter, setDateFilter] = useState(null);

  const filteredSourceFiles = useMemo(() => {
    return mockSourceFiles.filter(item => {
      const matchesFund = !fundFilter || item.fund.value === fundFilter;
      const matchesDate = !dateFilter || item.reportDate.value === dateFilter;
      return matchesFund && matchesDate;
    });
  }, [fundFilter, dateFilter]);

  const columns = [
    { key: 'name', label: 'FILE NAME', isEditable: false },
    { key: 'fund', label: 'FUND', isEditable: false },
    { key: 'reportDate', label: 'REPORT DATE', isEditable: false },
    { key: 'uploadedAt', label: 'UPLOADED AT', isEditable: false },
    { key: 'uploadedBy', label: 'UPLOADED BY', isEditable: false }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ background: '#fff', borderRadius: 8, padding: 24 }}>
        <div style={{ fontSize: 22, fontWeight: 600, marginBottom: 24 }}>Uploaded Source Files</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 18 }}>
          <span style={{ fontWeight: 500 }}>Filter by:</span>
          <select 
            value={fundFilter} 
            style={{ width: 140, padding: '4px 8px', borderRadius: 4, border: '1px solid #d9d9d9' }} 
            onChange={e => setFundFilter(e.target.value)}
          >
            <option value="">All Funds</option>
            {fundOptionsArray.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <input 
            type="date" 
            value={dateFilter || ''} 
            style={{ width: 130, padding: '4px 8px', borderRadius: 4, border: '1px solid #d9d9d9' }} 
            onChange={e => setDateFilter(e.target.value)} 
          />
          <UIComponents.Button 
            text="× Clear Filters" 
            onClick={() => { 
              setFundFilter(''); 
              setDateFilter(null); 
            }} 
          />
          <div style={{ flex: 1 }} />
          <UIComponents.Button text="View Archived" customStyle={{ background: '#2966d8', color: '#fff' }} />
          <UIComponents.Button 
            text="Archive Selected" 
            customStyle={{ background: '#ffe58f', color: '#ad6800' }}
            disabled={selectedRows.length === 0}
          />
          <UIComponents.Button 
            text="Delete Selected" 
            customStyle={{ background: '#ff7875', color: '#fff' }}
            disabled={selectedRows.length === 0}
          />
        </div>
        <DynamicTableComponents
          data={filteredSourceFiles}
          columns={columns}
          showSettings={false}
          onSelectionChange={setSelectedRows}
          selectable={true}
        />
        <div style={{ marginTop: 12, color: '#888', fontSize: 14 }}>
          {filteredSourceFiles.length} file(s)
          {selectedRows.length > 0 && `, ${selectedRows.length} selected`}
        </div>
      </div>
    </div>
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